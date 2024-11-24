"use client";
import { useEffect, useState, useRef } from "react";
import { Box, Button, Text, Heading, Image, Flex } from "@chakra-ui/react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { keyframes } from "@emotion/react";
import { use } from "react";

const pulse = keyframes`
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
`;

const pulseBackground = keyframes`
  0% { transform: scale(0.5); opacity: 0.5; }
  100% { transform: scale(1.5); opacity: 0; }
`;

export default function PatientPage({
  params,
}: {
  params: Promise<{ patientId: string }>;
}) {
  const { patientId } = use(params);
  const [isMounted, setIsMounted] = useState(false);
  const {
    transcript,
    listening,
    resetTranscript,
    isMicrophoneAvailable,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();
  const [forceUpdate, setForceUpdate] = useState(0);
  const [chatHistory, setChatHistory] = useState<
    { role: string; content: string }[]
  >([]);
  const [cumulativeTranscript, setCumulativeTranscript] = useState("");
  const [processedTranscripts, setProcessedTranscripts] = useState<Set<string>>(
    new Set()
  );
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const playAudioResponse = async (text: string) => {
    try {
      const options = {
        method: "POST",
        headers: {
          "xi-api-key": "sk_5bfd898b10d62dc9e595bb41daf17f4d2bcda1cbf6f1eb4a",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.5,
            style: 1,
          },
        }),
      };

      const response = await fetch(
        "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
        options
      );
      const audioBlob = await response.blob();
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);

      // Let the audio element handle playback through user interaction
      if (audioRef.current) {
        audioRef.current.onended = () => {
          URL.revokeObjectURL(url);
          setAudioUrl(null);
          SpeechRecognition.startListening();
        };
      }
    } catch (err) {
      console.error("Error with text-to-speech:", err);
      SpeechRecognition.startListening();
    }
  };

  useEffect(() => {
    setIsMounted(true);
    SpeechRecognition.startListening();

    return () => {
      SpeechRecognition.stopListening();
      resetTranscript();
    };
  }, []);

  useEffect(() => {
    if (
      !listening &&
      transcript.trim() &&
      !processedTranscripts.has(transcript)
    ) {
      // Mark this transcript as processed
      setProcessedTranscripts((prev) => new Set(prev).add(transcript));

      console.log("Transcript:", transcript);

      const newCumulativeTranscript = cumulativeTranscript + " " + transcript;
      setCumulativeTranscript(newCumulativeTranscript);

      const postData = {
        query: newCumulativeTranscript.trim(),
        history: chatHistory,
      };

      console.log("Sending POST request with data:", postData);

      fetch("http://127.0.0.1:8000/user/query/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Received response:", data);
          if (data.result) {
            const newHistory = [
              ...chatHistory,
              { role: "user", content: transcript.trim() },
              { role: "assistant", content: data.result },
            ];
            setChatHistory(newHistory);

            // Stop listening before playing audio
            SpeechRecognition.stopListening();
            // Play the response
            playAudioResponse(data.result);
          }
        })
        .catch((error) => {
          console.error("Error posting transcript:", error);
          SpeechRecognition.startListening();
        });

      // Remove the automatic restart of listening here since we'll handle it after audio plays
    } else if (!listening && !transcript.trim()) {
      // Restart listening if there's no transcript (timeout from silence)
      SpeechRecognition.startListening();
    }
  }, [
    listening,
    forceUpdate,
    transcript,
    chatHistory,
    cumulativeTranscript,
    processedTranscripts,
  ]);

  // Modify cleanup to also handle audio
  useEffect(() => {
    return () => {
      SpeechRecognition.stopListening();
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  if (!isMounted) {
    return null;
  }

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  if (!isMicrophoneAvailable) {
    return <span>Microphone not available.</span>;
  }

  return (
    <Box
      width="100%"
      height="calc(100vh - 100px)"
      display="flex"
      alignItems="center"
      justifyContent="center"
    >
      <Flex direction="column" align="center" justify="center" gap={4}>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
        >
          {listening && (
            <Text color="gray.500" fontSize="sm" mb={4}>
              Listening in background...
            </Text>
          )}
          <Box position="relative" width="100px" height="100px">
            <Box
              position="absolute"
              top="0"
              left="0"
              width="100%"
              height="100%"
              borderRadius="50%"
              background="gray"
              animation={
                listening ? `${pulseBackground} 1.5s infinite` : "none"
              }
            />
            <Box
              position="absolute"
              top="0"
              left="0"
              width="100%"
              height="100%"
              borderRadius="50%"
              background="radial-gradient(circle, rgba(240,240,240,1) 40%, transparent 30%), linear-gradient(to right, cyan, blue, purple)"
              border="none"
              animation={listening ? `${pulse} 1.5s infinite` : "none"}
            />
          </Box>
          <Text mt={4}>{transcript}</Text>
        </Box>

        {audioUrl && (
          <Box mt={4} width="300px">
            <audio
              ref={audioRef}
              controls
              autoPlay
              src={audioUrl}
              onEnded={() => {
                URL.revokeObjectURL(audioUrl);
                setAudioUrl(null);
                SpeechRecognition.startListening();
              }}
              style={{ width: "100%" }}
            />
          </Box>
        )}
      </Flex>
    </Box>
  );
}
