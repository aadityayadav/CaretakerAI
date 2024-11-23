"use client";
import { useEffect, useState } from "react";
import { Box, Button, Text, Heading, Image, Flex } from "@chakra-ui/react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { keyframes } from "@emotion/react";

const pulse = keyframes`
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
`;

const pulseBackground = keyframes`
  0% { transform: scale(0.5); opacity: 0.5; }
  100% { transform: scale(1.5); opacity: 0; }
`;

export default function Home() {
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
  }, []);

  if (!isMounted) {
    return null; // Render nothing on the server
  }

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  if (!isMicrophoneAvailable) {
    return <span>Microphone not available.</span>;
  }

  function toggleListening() {
    if (listening) {
      SpeechRecognition.stopListening();
    } else {
      SpeechRecognition.startListening({ continuous: true });
    }
  }

  return (
    <Box
      position="relative"
      height="100vh"
      background="radial-gradient(circle, rgba(220,220,235,1) 0%, rgba(230,230,255,1) 100%)"
    >
      <Box
        position="absolute"
        top="70px"
        left="50%"
        transform="translateX(-50%)"
        display="flex"
        flexDirection="row"
        alignItems="center"
        gap={2}
      >
        <Image src="/logo3.png" alt="CaretakerAI" width={55} />
        <Heading fontSize={"5xl"} fontWeight={"medium"}>
          CaretakerAI
        </Heading>
      </Box>

      <Flex
        direction="column"
        align="center"
        justify="center"
        height="100%"
        gap={4}
      >
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
        <Text>{transcript}</Text>
        <Button onClick={() => toggleListening()}>Start Listening</Button>
      </Flex>
    </Box>
  );
}

