"use client";
import { Box } from "@chakra-ui/react";
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/doctor/addPatient");
}
