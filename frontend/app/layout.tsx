// app/layout.tsx
"use client";
import "regenerator-runtime/runtime";
import { Providers } from "./providers";
import { ChakraProvider } from "@chakra-ui/react";
import "@fontsource/montserrat"; // Import Montserrat font
import { extendTheme } from "@chakra-ui/react";
import { Box } from "@chakra-ui/react";
import Header from "./components/header";
import { Image } from "@chakra-ui/react";
const theme = extendTheme({
  fonts: {
    heading: "Montserrat, sans-serif",
    body: "Montserrat, sans-serif",
  },
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ChakraProvider theme={theme}>
          <Providers>
            <Box position="relative" minHeight="100vh">
              <Image
                src="/hero-top.jpg"
                alt="hero"
                position="absolute"
                top="0"
                left="0"
                width="100%"
                height="100%"
                objectFit="cover"
                zIndex={0}
              />
              <Box
                position="relative"
                background="transparent"
                minHeight="100vh"
                height="100%"
                padding={4}
              >
                <Box
                  maxWidth="1200px"
                  margin="0 auto"
                  display="flex"
                  flexDirection="column"
                  gap={4}
                >
                  <Header />
                  <Box
                    borderRadius="10px"
                    backdropFilter="blur(16px)"
                    backgroundColor="rgba(255, 255, 255, 0.35)"
                    border="1px solid rgba(255, 255, 255, 0.2)"
                    padding={4}
                    display="grid"
                    flexDirection="column"
                    minHeight="100vh"
                    height="100%"
                    boxShadow="0 4px 6px rgba(0, 0, 0, 0.1)"
                  >
                    {children}
                  </Box>
                </Box>
              </Box>
            </Box>
          </Providers>
        </ChakraProvider>
      </body>
    </html>
  );
}
