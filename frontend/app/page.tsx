"use client";
import { useEffect, useState } from "react";
import { Box, Button, Text, Heading, Image, Flex } from "@chakra-ui/react";
import Listen from "./components/listen";
import Header from "./components/header";
import SignUp from "./components/signUp";
export default function Home() {
  const [page, setPage] = useState("listen");

  return (
    <Box
      background="radial-gradient(circle, rgba(220,220,235,1) 0%, rgba(230,230,255,1) 100%)"
      height="100vh"
    >
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        width="80%"
        margin="0 auto"
      >
        <br/>
        <Header />
        {page === "signUp" && <SignUp />}
        {page === "listen" && <Listen />}
      </Box>
    </Box>
  );
}
