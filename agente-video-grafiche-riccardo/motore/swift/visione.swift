// visione — Apple Vision sui fotogrammi del girato.
//
//   visione volti  <video> <passo_s> <out.json> [t0 t1]
//       volto per volto: riquadro, qualita dello scatto, orientamento, apertura occhi
//   visione sagome <cartella_png> <cartella_maschere>
//       sagoma della persona (maschera in scala di grigi, stessa misura del frame)
//   visione posa <out.json> <immagine>...
//       punti del corpo (orecchio, spalla, anca, ginocchio, caviglia, naso, collo) su
//       immagini ferme, con l'orientamento EXIF; per persona, ogni punto con confidenza
//
// I riquadri escono normalizzati con origine IN ALTO a sinistra (Vision li da
// con origine in basso: qui si girano una volta per tutte).

import AVFoundation
import CoreImage
import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

func fail(_ s: String) -> Never {
    FileHandle.standardError.write((s + "\n").data(using: .utf8)!)
    exit(1)
}

func eyeOpen(_ r: VNFaceLandmarkRegion2D?) -> Double {
    guard let r = r, r.pointCount >= 4 else { return -1 }
    let p = r.normalizedPoints
    let xs = p.map { Double($0.x) }, ys = p.map { Double($0.y) }
    let w = (xs.max()! - xs.min()!), h = (ys.max()! - ys.min()!)
    return w > 0 ? h / w : -1
}

func faces(_ img: CGImage) -> [[String: Any]] {
    let q = VNDetectFaceCaptureQualityRequest()
    let lm = VNDetectFaceLandmarksRequest()
    let h = VNImageRequestHandler(cgImage: img, options: [:])
    do { try h.perform([lm]) } catch { return [] }
    let found = lm.results ?? []
    if !found.isEmpty {
        q.inputFaceObservations = found
        try? h.perform([q])
    }
    let qual = q.results ?? []
    var out: [[String: Any]] = []
    for (i, f) in found.enumerated() {
        let b = f.boundingBox
        var d: [String: Any] = [
            "x": Double(b.minX), "y": Double(1 - b.maxY), "w": Double(b.width), "h": Double(b.height),
            "conf": Double(f.confidence),
        ]
        if i < qual.count, let fq = qual[i].faceCaptureQuality { d["q"] = Double(fq) }
        if let y = f.yaw { d["yaw"] = y.doubleValue }
        if let p = f.pitch { d["pitch"] = p.doubleValue }
        if let r = f.roll { d["roll"] = r.doubleValue }
        if let l = f.landmarks {
            d["occhio_sx"] = eyeOpen(l.leftEye)
            d["occhio_dx"] = eyeOpen(l.rightEye)
            d["bocca"] = eyeOpen(l.outerLips)
        }
        out.append(d)
    }
    return out
}

func volti(_ args: [String]) {
    guard args.count >= 3 else { fail("uso: visione volti <video> <passo_s> <out.json> [t0 t1]") }
    let url = URL(fileURLWithPath: args[0])
    let step = Double(args[1])!
    let asset = AVURLAsset(url: url)
    let dur = CMTimeGetSeconds(asset.duration)
    let t0 = args.count > 3 ? Double(args[3])! : 0
    let t1 = args.count > 4 ? min(Double(args[4])!, dur) : dur
    var times: [Double] = []
    var t = t0
    while t < t1 { times.append(t); t += step }
    var results = [[String: Any]?](repeating: nil, count: times.count)
    let lock = NSLock()
    let workers = 6
    var done = 0
    DispatchQueue.concurrentPerform(iterations: workers) { w in
        let gen = AVAssetImageGenerator(asset: asset)
        gen.appliesPreferredTrackTransform = true
        let tol = CMTime(seconds: step / 4, preferredTimescale: 600)
        gen.requestedTimeToleranceBefore = tol
        gen.requestedTimeToleranceAfter = tol
        gen.maximumSize = CGSize(width: 1920, height: 1920)
        var i = w
        while i < times.count {
            var actual = CMTime.zero
            if let img = try? gen.copyCGImage(at: CMTime(seconds: times[i], preferredTimescale: 600),
                                              actualTime: &actual) {
                let r: [String: Any] = ["t": CMTimeGetSeconds(actual), "volti": faces(img),
                                        "w": img.width, "h": img.height]
                lock.lock(); results[i] = r; done += 1
                if done % 200 == 0 { FileHandle.standardError.write("  \(done)/\(times.count)\n".data(using: .utf8)!) }
                lock.unlock()
            }
            i += workers
        }
    }
    let arr = results.compactMap { $0 }
    let data = try! JSONSerialization.data(withJSONObject: ["durata": dur, "passo": step, "campioni": arr])
    try! data.write(to: URL(fileURLWithPath: args[2]))
}

func sagome(_ args: [String]) {
    guard args.count >= 2 else { fail("uso: visione sagome <cartella_png> <cartella_maschere>") }
    let inDir = URL(fileURLWithPath: args[0]), outDir = URL(fileURLWithPath: args[1])
    try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
    let files = (try! FileManager.default.contentsOfDirectory(atPath: inDir.path))
        .filter { $0.hasSuffix(".png") }.sorted()
    let ctx = CIContext()
    DispatchQueue.concurrentPerform(iterations: files.count) { i in
        let f = files[i]
        guard let src = CGImageSourceCreateWithURL(inDir.appendingPathComponent(f) as CFURL, nil),
              let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { return }
        let req = VNGeneratePersonSegmentationRequest()
        req.qualityLevel = .accurate
        req.outputPixelFormat = kCVPixelFormatType_OneComponent8
        let h = VNImageRequestHandler(cgImage: img, options: [:])
        guard (try? h.perform([req])) != nil, let m = req.results?.first?.pixelBuffer else { return }
        var ci = CIImage(cvPixelBuffer: m)
        let sx = CGFloat(img.width) / ci.extent.width, sy = CGFloat(img.height) / ci.extent.height
        ci = ci.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
        guard let cg = ctx.createCGImage(ci, from: CGRect(x: 0, y: 0, width: img.width, height: img.height),
                                         format: .L8, colorSpace: CGColorSpaceCreateDeviceGray()) else { return }
        let dst = CGImageDestinationCreateWithURL(outDir.appendingPathComponent(f) as CFURL,
                                                  UTType.png.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(dst, cg, nil)
        CGImageDestinationFinalize(dst)
    }
}

let giunture: [(String, VNHumanBodyPoseObservation.JointName)] = [
    ("orecchio_sx", .leftEar), ("orecchio_dx", .rightEar), ("spalla_sx", .leftShoulder), ("spalla_dx", .rightShoulder),
    ("anca_sx", .leftHip), ("anca_dx", .rightHip), ("ginocchio_sx", .leftKnee), ("ginocchio_dx", .rightKnee),
    ("caviglia_sx", .leftAnkle), ("caviglia_dx", .rightAnkle), ("naso", .nose), ("collo", .neck)]

func posa(_ args: [String]) {
    guard args.count >= 2 else { fail("uso: visione posa <out.json> <immagine>...") }
    var righe: [[String: Any]] = []
    for path in args.dropFirst() {
        guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
              let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fail("immagine illeggibile: \(path)") }
        let props = CGImageSourceCopyPropertiesAtIndex(src, 0, nil) as? [CFString: Any]
        let ori = (props?[kCGImagePropertyOrientation] as? UInt32).flatMap { CGImagePropertyOrientation(rawValue: $0) } ?? .up
        let req = VNDetectHumanBodyPoseRequest()
        try? VNImageRequestHandler(cgImage: img, orientation: ori, options: [:]).perform([req])
        var persone: [[String: Any]] = []
        for o in req.results ?? [] {
            var p: [String: Any] = [:]
            for (n, j) in giunture {
                if let pt = try? o.recognizedPoint(j), pt.confidence > 0 {
                    p[n] = ["x": Double(pt.location.x), "y": Double(1 - pt.location.y), "conf": Double(pt.confidence)]
                }
            }
            persone.append(p)
        }
        righe.append(["file": path, "persone": persone])
    }
    let data = try! JSONSerialization.data(withJSONObject: righe)
    try! data.write(to: URL(fileURLWithPath: args[0]))
}

// mani: per ogni PNG della cartella (uno ogni `passo`), le mani trovate da Vision:
// centro (media dei punti sicuri), riquadro dei punti, polso, lato (sx/dx della
// persona). Coordinate normalizzate, origine in alto a sinistra.
func mani(_ args: [String]) {
    guard args.count >= 2 else { fail("uso: visione mani <cartella_png> <out.json> [passo]") }
    let inDir = URL(fileURLWithPath: args[0])
    let passo = args.count > 2 ? Int(args[2]) ?? 1 : 1
    let files = (try! FileManager.default.contentsOfDirectory(atPath: inDir.path))
        .filter { $0.hasSuffix(".png") }.sorted()
    let scelti = stride(from: 0, to: files.count, by: max(1, passo)).map { files[$0] }
    var out = [[String: Any]?](repeating: nil, count: scelti.count)
    let lock = NSLock()
    DispatchQueue.concurrentPerform(iterations: scelti.count) { i in
        let f = scelti[i]
        guard let src = CGImageSourceCreateWithURL(inDir.appendingPathComponent(f) as CFURL, nil),
              let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { return }
        let req = VNDetectHumanHandPoseRequest()
        req.maximumHandCount = 2
        try? VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
        var hands: [[String: Any]] = []
        for o in req.results ?? [] {
            guard let pts = try? o.recognizedPoints(.all) else { continue }
            let ok = pts.values.filter { $0.confidence > 0.3 }
            if ok.count < 6 { continue }
            let xs = ok.map { Double($0.location.x) }, ys = ok.map { 1 - Double($0.location.y) }
            var h: [String: Any] = [
                "x": xs.reduce(0, +) / Double(xs.count), "y": ys.reduce(0, +) / Double(ys.count),
                "box": [xs.min()!, ys.min()!, xs.max()!, ys.max()!], "punti": ok.count,
                "lato": o.chirality == .left ? "sx" : (o.chirality == .right ? "dx" : "?")]
            if let w = pts[.wrist], w.confidence > 0.3 { h["polso"] = [Double(w.location.x), 1 - Double(w.location.y)] }
            hands.append(h)
        }
        lock.lock(); out[i] = ["file": f, "mani": hands]; lock.unlock()
    }
    let data = try! JSONSerialization.data(withJSONObject: out.compactMap { $0 })
    try! data.write(to: URL(fileURLWithPath: args[1]))
}

let a = Array(CommandLine.arguments.dropFirst())
guard let cmd = a.first else { fail("uso: visione volti|sagome|posa|mani ...") }
switch cmd {
case "volti": volti(Array(a.dropFirst()))
case "sagome": sagome(Array(a.dropFirst()))
case "posa": posa(Array(a.dropFirst()))
case "mani": mani(Array(a.dropFirst()))
default: fail("comando sconosciuto: \(cmd)")
}
