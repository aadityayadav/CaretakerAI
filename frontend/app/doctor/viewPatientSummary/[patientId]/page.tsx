"use client";
import { Box, Image, Heading } from "@chakra-ui/react";
import { use, useState } from "react";
import Ai from "@/app/components/ai";
import { Text, Divider } from "@chakra-ui/react";

// Import the MedicalRecord type from Ai component
interface MedicalRecord {
  symptoms?: {
    description: string;
    date: string;
  }[];
  allergies?: {
    name: string;
    date: string;
  }[];
  past_diagnoses?: {
    name: string;
    description: string;
    doctor_name: string;
    date: string;
  }[];
  medications?: {
    name: string;
    date: string;
    description: string;
    dosage?: string;
    frequency?: string;
  }[];
}

export default function ViewPatientSummary({
  params,
}: {
  params: Promise<{ patientId: string }>;
}) {
  const { patientId } = use(params);
  const [medicalData, setMedicalData] = useState<MedicalRecord | null>(null);

  return (
    <Box height={"100%"} display="flex" flexDirection="row" gap={4}>
      <Box
        width={"50%"}
        bg="whiteAlpha.500"
        padding={4}
        borderRadius="lg"
        boxShadow="sm"
      >
        <Heading>Patient Summary: Alice</Heading>
        <Divider my={2} borderColor="blackAlpha.500" />

        {medicalData ? (
          <Box>
            {/* Display medical data sections */}
            {medicalData.symptoms && medicalData.symptoms.length > 0 && (
              <Box mb={4}>
                <Heading size="md" mb={2}>Symptoms</Heading>
                {medicalData.symptoms.map((symptom, index) => (
                  <Text key={index}>
                    {symptom.description} - {new Date(symptom.date).toLocaleDateString()}
                  </Text>
                ))}
              </Box>
            )}
            
            {medicalData.allergies && medicalData.allergies.length > 0 && (
              <Box mb={4}>
                <Heading size="md" mb={2}>Allergies</Heading>
                {medicalData.allergies.map((allergy, index) => (
                  <Text key={index}>
                    {allergy.name} - {new Date(allergy.date).toLocaleDateString()}
                  </Text>
                ))}
              </Box>
            )}
            
            {medicalData.past_diagnoses && medicalData.past_diagnoses.length > 0 && (
              <Box mb={4}>
                <Heading size="md" mb={2}>Past Diagnoses</Heading>
                {medicalData.past_diagnoses.map((diagnosis, index) => (
                  <Box key={index} mb={2}>
                    <Text fontWeight="bold">{diagnosis.name}</Text>
                    <Text>Description: {diagnosis.description}</Text>
                    <Text>Doctor: {diagnosis.doctor_name}</Text>
                    <Text>Date: {new Date(diagnosis.date).toLocaleDateString()}</Text>
                  </Box>
                ))}
              </Box>
            )}
            
            {medicalData.medications && medicalData.medications.length > 0 && (
              <Box mb={4}>
                <Heading size="md" mb={2}>Medications</Heading>
                {medicalData.medications.map((medication, index) => (
                  <Box key={index} mb={2}>
                    <Text fontWeight="bold">{medication.name}</Text>
                    <Text>Description: {medication.description}</Text>
                    {medication.dosage && <Text>Dosage: {medication.dosage}</Text>}
                    {medication.frequency && <Text>Frequency: {medication.frequency}</Text>}
                    <Text>Date: {new Date(medication.date).toLocaleDateString()}</Text>
                  </Box>
                ))}
              </Box>
            )}
          </Box>
        ) : (
          <Text>
            Ask the AI assistant to retrieve patient information.
          </Text>
        )}
      </Box>
      <Box width={"50%"} pt={4}>
        <Ai 
          params={{ userId: patientId, isDoctor: true, onMedicalDataUpdate: setMedicalData }}
        />
      </Box>
    </Box>
  );  
}
