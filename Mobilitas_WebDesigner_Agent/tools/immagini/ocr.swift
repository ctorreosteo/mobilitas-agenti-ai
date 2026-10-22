import Foundation
import Vision
import AppKit
// OCR locale (Vision di macOS) su ogni immagine passata come argomento; stampa "file<TAB>testo".
for path in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
  let req = VNRecognizeTextRequest()
  req.recognitionLevel = .accurate
  req.recognitionLanguages = ["it-IT"]
  try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
  let text = (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: " ")
  print("\((path as NSString).lastPathComponent)\t\(text)")
}
