// testo <cartella_png> <out.json> <y_offset_px>: Apple Vision VNRecognizeTextRequest su ogni PNG
import Foundation
import Vision
import ImageIO
let a = CommandLine.arguments
let dir = URL(fileURLWithPath: a[1]); let yoff = Double(a[3])!
let files = try! FileManager.default.contentsOfDirectory(atPath: dir.path).filter { $0.hasSuffix(".png") }.sorted()
var res = [[String: Any]](repeating: [:], count: files.count)
let lock = NSLock()
DispatchQueue.concurrentPerform(iterations: files.count) { i in
    let u = dir.appendingPathComponent(files[i])
    guard let src = CGImageSourceCreateWithURL(u as CFURL, nil), let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { return }
    let W = Double(img.width), H = Double(img.height)
    let r = VNRecognizeTextRequest(); r.recognitionLevel = .accurate; r.recognitionLanguages = ["it-IT"]; r.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: img, options: [:]).perform([r])
    var obs: [[String: Any]] = []
    for o in r.results ?? [] {
        guard let c = o.topCandidates(1).first else { continue }
        let b = o.boundingBox
        obs.append(["t": c.string, "conf": Double(c.confidence),
                    "x": b.minX * W, "y": (1 - b.maxY) * H + yoff, "w": b.width * W, "h": b.height * H])
    }
    lock.lock(); res[i] = ["file": files[i], "obs": obs]; lock.unlock()
}
let d = try! JSONSerialization.data(withJSONObject: res, options: [.prettyPrinted])
try! d.write(to: URL(fileURLWithPath: a[2]))
print(files.count, "immagini")
