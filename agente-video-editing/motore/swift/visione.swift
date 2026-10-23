// visione — Apple Vision sui fotogrammi del girato.
//
//   visione volti  <video> <passo_s> <out.json> [t0 t1]
//       volto per volto: riquadro, qualita dello scatto, orientamento, apertura occhi
//   visione sagome <cartella_png> <cartella_maschere>
//       sagoma della persona (maschera in scala di grigi, stessa misura del frame)
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

let a = Array(CommandLine.arguments.dropFirst())
guard let cmd = a.first else { fail("uso: visione volti|sagome ...") }
switch cmd {
case "volti": volti(Array(a.dropFirst()))
case "sagome": sagome(Array(a.dropFirst()))
default: fail("comando sconosciuto: \(cmd)")
}
