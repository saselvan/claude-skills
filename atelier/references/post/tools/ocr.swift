#!/usr/bin/swift
import Vision
import Foundation

guard CommandLine.arguments.count > 1 else {
    print("Usage: ocr.swift <image_path>", to: &standardError)
    exit(1)
}

let imagePath = CommandLine.arguments[1]
guard let cgImage = NSImage(contentsOfFile: imagePath)?.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Error: Could not load image", to: &standardError)
    exit(1)
}

var recognizedText = ""
let request = VNRecognizeTextRequest()
request.recognitionLanguages = ["en-US"]

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
do {
    try handler.perform([request])
    if let results = request.results as? [VNRecognizedTextObservation] {
        for observation in results {
            if let topCandidate = observation.topCandidates(1).first {
                recognizedText += topCandidate.string + "\n"
            }
        }
    }
    print(recognizedText)
} catch {
    print("Error: \(error.localizedDescription)", to: &standardError)
    exit(1)
}
