"use client";
import { useEffect, useState, useRef } from "react";
import { Box, Button, Text, Heading, Image, Flex } from "@chakra-ui/react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { keyframes } from "@emotion/react";
import { use } from "react";
import { ArrowForwardIcon } from "@chakra-ui/icons";

const pulse = keyframes`
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
`;

const pulseBackground = keyframes`
  0% { transform: scale(1); opacity: 0.15; }
  100% { transform: scale(1.5); opacity: 0; }
`;

interface MedicalRecord {
  symptoms?: {
    description: string;
    date: string;
  }[];
  allergies?: {
    name: string;
    date: string;
  }[];
  past_diagnoses?: {
    name: string;
    description: string;
    doctor_name: string;
    date: string;
  }[];
  medications?: {
    name: string;
    date: string;
    description: string;
    dosage?: string;
    frequency?: string;
  }[];
}

interface AiProps {
  params: {
    userId: string;
    isDoctor: boolean;
    onMedicalDataUpdate?: (data: MedicalRecord) => void;
  };
}

export default function Ai({ params }: AiProps) {
  const { userId, isDoctor, onMedicalDataUpdate } = params;
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
  const [isActivated, setIsActivated] = useState(false);

  const playAudioResponse = async (text: string) => {
    try {
      const options = {
        method: "POST",
        headers: {
          "xi-api-key": "sk_eb960fcbd5eb6694d25dba3860aa532d24fd4ab81406a92a",
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

      const voiceId = isDoctor
        ? "onwK4e9ZLuTAKqWW03F9"
        : "EXAVITQu4vr4xnSDxMaL";
      const response = await fetch(
        `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
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
    return () => {
      SpeechRecognition.stopListening();
      resetTranscript();
    };
  }, []);

  const handleActivate = () => {
    setIsActivated(true);
    SpeechRecognition.startListening();
  };

  useEffect(() => {
    if (!isActivated) return;

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
        query: transcript.trim(),
        history: chatHistory,
      };

      console.log("Sending POST request with data:", postData);

      fetch(`http://127.0.0.1:8000/${isDoctor ? "doctor" : "user"}/query/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Received response:", data);

          if (
            typeof data.result === "object" &&
            isDoctor &&
            onMedicalDataUpdate
          ) {
            onMedicalDataUpdate(data.result);
            if (data.summary) {
              playAudioResponse(data.summary);
            }
          } else if (data.result) {
            if (data.result.toLowerCase() === 'hello') {
              SpeechRecognition.startListening();
              return
            }
            const newHistory = [
              ...chatHistory,
              { role: "user", content: transcript.trim() },
              { role: "assistant", content: data.result },
            ];
            setChatHistory(newHistory);
            SpeechRecognition.stopListening();
            playAudioResponse(data.result);
          }
        })
        .catch((error) => {
          console.error("Error posting transcript:", error);
          SpeechRecognition.startListening();
        });

      // Remove the automatic restart of listening here since we'll handle it after audio plays
    } else if (!listening && !transcript.trim() && isActivated) {
      // Only restart listening if activated
      SpeechRecognition.startListening();
    }
  }, [
    listening,
    forceUpdate,
    transcript,
    chatHistory,
    cumulativeTranscript,
    processedTranscripts,
    isActivated,
    onMedicalDataUpdate,
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
        {!isActivated ? (
          <Button
            position="relative"
            bg={isDoctor ? "#FB8B24" : "#0081FB"}
            color="white"
            _hover={{ bg: isDoctor ? "#e07d20" : "#006ee0" }}
            size="lg"
            onClick={handleActivate}
            borderRadius="full"
            rightIcon={<ArrowForwardIcon />}
            minW="180px"
            h="48px"
            _before={{
              content: '""',
              position: "absolute",
              inset: "-4px",
              borderRadius: "full",
              background: isDoctor ? "#FB8B24" : "#0081FB",
              animation: `${pulseBackground} 2.5s infinite`,
              zIndex: -1,
            }}
          >
            {isDoctor ? "Activate Doctor" : "Activate Caretaker"}
          </Button>
        ) : (
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
                background={
                  isDoctor
                    ? "radial-gradient(circle, rgba(240,240,240,1) 40%, transparent 30%), linear-gradient(to right, #FFB347, #FB8B24, #CC5500)"
                    : "radial-gradient(circle, rgba(240,240,240,1) 40%, transparent 30%), linear-gradient(to right, cyan, blue, purple)"
                }
                border="none"
                animation={listening ? `${pulse} 1.5s infinite` : "none"}
              />
            </Box>
            <Text mt={4}>{transcript}</Text>
          </Box>
        )}

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
