"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { Box, Button } from "@chakra-ui/react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { keyframes } from "@emotion/react";
import { useState } from "react";

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
  const [isPulsating, setIsPulsating] = useState(true);

  return (
    <Box
      display="flex"
      flexDirection="row"
      alignItems={"center"}
      justifyContent={"center"}
      height="100vh"
    >
      <Box display="flex" flexDirection="column" alignItems={"center"} gap={12}>
        <Box position="relative" width="100px" height="100px">
          <Box
            position="absolute"
            top="0"
            left="0"
            width="100%"
            height="100%"
            borderRadius="50%"
            background="gray"
            animation={isPulsating ? `${pulseBackground} 1.5s infinite` : "none"}
          />
          <Box
            position="absolute"
            top="0"
            left="0"
            width="100%"
            height="100%"
            borderRadius="50%"
            background="radial-gradient(circle, white 40%, transparent 30%), linear-gradient(to right, cyan, blue, purple)"
            border="none"
            animation={isPulsating ? `${pulse} 1.5s infinite` : "none"}
          />
        </Box>

        <Button onClick={() => setIsPulsating(!isPulsating)}>Toggle Pulse</Button>
      </Box>
    </Box>
  );
}
