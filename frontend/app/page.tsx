"use client";
import { Box } from "@chakra-ui/react";
import { redirect } from "next/navigation";
import Header from "./components/Header";

export default function Home() {
  redirect("/doctor/addPatient");
}
