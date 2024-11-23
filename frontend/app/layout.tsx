// app/layout.tsx
"use client";
import "regenerator-runtime/runtime";
import { Providers } from "./providers";
import { ChakraProvider } from "@chakra-ui/react";
import "@fontsource/montserrat"; // Import Montserrat font
import { extendTheme } from "@chakra-ui/react";
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
          <Providers>{children}</Providers>
        </ChakraProvider>
      </body>
    </html>
  );
}
