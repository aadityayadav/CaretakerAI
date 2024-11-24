// app/layout.tsx
"use client";
import "regenerator-runtime/runtime";
import { Providers } from "./providers";
import { ChakraProvider } from "@chakra-ui/react";
import "@fontsource/montserrat"; // Import Montserrat font
import { extendTheme } from "@chakra-ui/react";
import { Box } from "@chakra-ui/react";
import Header from "./components/header";

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
            <Box
              background="radial-gradient(circle, rgba(220,220,235,1) 0%, rgba(230,230,255,1) 100%)"
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
                {children}
              </Box>
            </Box>
          </Providers>
        </ChakraProvider>
      </body>
    </html>
  );
}
