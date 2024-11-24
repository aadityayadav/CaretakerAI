"use client";
import { Box, Image, Heading } from "@chakra-ui/react";
import {use } from "react"

export default function ViewPatientSummary({
  params,
}: {
  params: Promise<{ patientId: string }>;
}) {
  const { patientId } = use(params);
  return <>View Patient Summary {patientId}</>;
}
