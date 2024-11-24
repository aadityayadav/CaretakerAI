"use client";
import { useEffect, useState } from "react";
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

  useEffect(() => {
    setIsMounted(true);
    SpeechRecognition.startListening({ continuous: true });

    return () => {
      SpeechRecognition.stopListening();
      resetTranscript();
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
              animation={listening ? `${pulseBackground} 1.5s infinite` : "none"}
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
      </Flex>
    </Box>
  );
}
