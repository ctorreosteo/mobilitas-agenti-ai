// persona — Apple Vision fotogramma per fotogramma per l'agente reel-grafiche (fase 6, 05/11/2026).
//
//   persona <cartella_jpg> <out.json> <cartella_maschere>
//
// Per ogni immagine della cartella (un fotogramma del reel, di solito a metà risoluzione):
// - volti: riquadro e confidenza;
// - mani: riquadro dei punti sicuri;
// - testa: naso, occhi, orecchie, collo (posa del corpo), per stimare la cima della testa;
// - sagoma: maschera della persona (VNGeneratePersonSegmentationRequest, .balanced), salvata come PNG
//   in scala di grigi a 1/4 della misura dell'immagine nella cartella delle maschere, più riquadro e copertura.
// I riquadri escono normalizzati (0-1) con origine IN ALTO a sinistra.
// File nuovo: il motore YouTube (visione.swift) non cambia.

import CoreImage
import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

func fail(_ s: String) -> Never {
    FileHandle.standardError.write((s + "\n").data(using: .utf8)!)
    exit(1)
}

let a = CommandLine.arguments
guard a.count >= 4 else { fail("uso: persona <cartella_jpg> <out.json> <cartella_maschere>") }
let inDir = URL(fileURLWithPath: a[1]), outJson = URL(fileURLWithPath: a[2]), mDir = URL(fileURLWithPath: a[3])
try? FileManager.default.createDirectory(at: mDir, withIntermediateDirectories: true)
let files = (try! FileManager.default.contentsOfDirectory(atPath: inDir.path))
    .filter { $0.hasSuffix(".jpg") || $0.hasSuffix(".png") }.sorted()
var res = [[String: Any]?](repeating: nil, count: files.count)
let lock = NSLock()
let punti: [(String, VNHumanBodyPoseObservation.JointName)] = [
    ("naso", .nose), ("occhio_sx", .leftEye), ("occhio_dx", .rightEye), ("orecchio_sx", .leftEar),
    ("orecchio_dx", .rightEar), ("collo", .neck), ("spalla_sx", .leftShoulder), ("spalla_dx", .rightShoulder)]

DispatchQueue.concurrentPerform(iterations: files.count) { i in
    let f = files[i]
    let ctx = CIContext()
    guard let src = CGImageSourceCreateWithURL(inDir.appendingPathComponent(f) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { return }
    let h = VNImageRequestHandler(cgImage: img, options: [:])
    let fr = VNDetectFaceRectanglesRequest()
    let hr = VNDetectHumanHandPoseRequest(); hr.maximumHandCount = 4
    let br = VNDetectHumanBodyPoseRequest()
    let sr = VNGeneratePersonSegmentationRequest()
    sr.qualityLevel = .balanced
    sr.outputPixelFormat = kCVPixelFormatType_OneComponent8
    try? h.perform([fr, hr, br, sr])
    var volti: [[String: Any]] = []
    for o in fr.results ?? [] {
        let b = o.boundingBox
        volti.append(["x": Double(b.minX), "y": Double(1 - b.maxY), "w": Double(b.width), "h": Double(b.height),
                      "conf": Double(o.confidence)])
    }
    var mani: [[String: Any]] = []
    for o in hr.results ?? [] {
        guard let pts = try? o.recognizedPoints(.all) else { continue }
        let ok = pts.values.filter { $0.confidence > 0.3 }
        if ok.count < 6 { continue }
        let xs = ok.map { Double($0.location.x) }, ys = ok.map { 1 - Double($0.location.y) }
        mani.append(["box": [xs.min()!, ys.min()!, xs.max()!, ys.max()!], "punti": ok.count])
    }
    var teste: [[String: Any]] = []
    for o in br.results ?? [] {
        var p: [String: Any] = [:]
        for (n, j) in punti {
            if let pt = try? o.recognizedPoint(j), pt.confidence > 0.2 {
                p[n] = [Double(pt.location.x), 1 - Double(pt.location.y), Double(pt.confidence)]
            }
        }
        if !p.isEmpty { teste.append(p) }
    }
    var sagoma: [String: Any] = ["copertura": 0.0]
    if let m = sr.results?.first?.pixelBuffer {
        let mw = max(1, img.width / 4), mh = max(1, img.height / 4)
        var ci = CIImage(cvPixelBuffer: m)
        ci = ci.transformed(by: CGAffineTransform(scaleX: CGFloat(mw) / ci.extent.width, y: CGFloat(mh) / ci.extent.height))
        if let cg = ctx.createCGImage(ci, from: CGRect(x: 0, y: 0, width: mw, height: mh), format: .L8,
                                      colorSpace: CGColorSpaceCreateDeviceGray()) {
            // copertura e riquadro (pixel > 127)
            var buf = [UInt8](repeating: 0, count: mw * mh)
            let bctx = CGContext(data: &buf, width: mw, height: mh, bitsPerComponent: 8, bytesPerRow: mw,
                                 space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
            bctx.draw(cg, in: CGRect(x: 0, y: 0, width: mw, height: mh))
            var n = 0, x0 = mw, y0 = mh, x1 = -1, y1 = -1
            for y in 0..<mh { for x in 0..<mw where buf[y * mw + x] > 127 {
                n += 1; x0 = min(x0, x); x1 = max(x1, x); y0 = min(y0, y); y1 = max(y1, y) } }
            sagoma["copertura"] = Double(n) / Double(mw * mh)
            if n > 0 {
                sagoma["box"] = [Double(x0) / Double(mw), Double(y0) / Double(mh), Double(x1 + 1) / Double(mw), Double(y1 + 1) / Double(mh)]
            }
            let nome = (f as NSString).deletingPathExtension + ".png"
            let dst = CGImageDestinationCreateWithURL(mDir.appendingPathComponent(nome) as CFURL,
                                                      UTType.png.identifier as CFString, 1, nil)!
            CGImageDestinationAddImage(dst, cg, nil)
            CGImageDestinationFinalize(dst)
            sagoma["maschera"] = nome
        }
    }
    lock.lock()
    res[i] = ["file": f, "volti": volti, "mani": mani, "teste": teste, "sagoma": sagoma]
    lock.unlock()
}
let d = try! JSONSerialization.data(withJSONObject: res.compactMap { $0 })
try! d.write(to: outJson)
print(files.count, "immagini")
