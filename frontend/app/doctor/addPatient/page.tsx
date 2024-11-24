"use client";
import { useState } from "react";
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  NumberInput,
  NumberInputField,
  Select,
  VStack,
  Container,
  Heading,
  useToast,
} from "@chakra-ui/react";

export default function AddPatient() {
  const toast = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    age: "",
    gender: "",
    weight: "",
    height: "",
    symptoms: [
      {
        description: "",
        date: new Date().toISOString().split('T')[0],
      },
    ],
    past_diagnoses: [
      {
        name: "",
        description: "",
        doctor_name: "",
        date: new Date().toISOString().split('T')[0],
      },
    ],
    allergies: [],
    medications: [],
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSymptomChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      symptoms: [
        {
          ...prev.symptoms[0],
          [field]: value,
        },
      ],
    }));
  };

  const handleDiagnosisChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      past_diagnoses: [
        {
          ...prev.past_diagnoses[0],
          [field]: value,
        },
      ],
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(JSON.stringify(formData, null, 2));
    toast({
      title: "Form submitted",
      description: "Check console for form data",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <Container maxW="container.md" py={8}>
      <VStack spacing={8} as="form" onSubmit={handleSubmit}>
        <Heading size="lg" color="teal.600">Add New Patient</Heading>

        {/* Basic Information */}
        <Box 
          w="100%" 
          p={6} 
          borderWidth={1} 
          borderRadius="lg" 
          shadow="sm"
          bg="white"
          borderColor="teal.200"
        >
          <VStack spacing={4}>
            <Heading size="md" color="teal.500" mb={2}>Basic Information</Heading>
            <FormControl isRequired>
              <FormLabel color="gray.700">Full Name</FormLabel>
              <Input
                value={formData.name}
                onChange={(e) => handleInputChange("name", e.target.value)}
                borderColor="gray.300"
                _hover={{ borderColor: "teal.300" }}
                _focus={{ borderColor: "teal.500", boxShadow: "0 0 0 1px teal.500" }}
              />
            </FormControl>

            <FormControl isRequired>
              <FormLabel color="gray.700">Email</FormLabel>
              <Input
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange("email", e.target.value)}
                borderColor="gray.300"
                _hover={{ borderColor: "teal.300" }}
                _focus={{ borderColor: "teal.500", boxShadow: "0 0 0 1px teal.500" }}
              />
            </FormControl>

            <FormControl isRequired>
              <FormLabel color="gray.700">Age</FormLabel>
              <NumberInput min={0} max={150}>
                <NumberInputField
                  value={formData.age}
                  onChange={(e) => handleInputChange("age", e.target.value)}
                />
              </NumberInput>
            </FormControl>

            <FormControl isRequired>
              <FormLabel color="gray.700">Gender</FormLabel>
              <Select
                placeholder="Select gender"
                value={formData.gender}
                onChange={(e) => handleInputChange("gender", e.target.value)}
                borderColor="gray.300"
                _hover={{ borderColor: "teal.300" }}
                _focus={{ borderColor: "teal.500", boxShadow: "0 0 0 1px teal.500" }}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </Select>
            </FormControl>

            <FormControl>
              <FormLabel>Weight (kg)</FormLabel>
              <NumberInput min={0} precision={1}>
                <NumberInputField
                  value={formData.weight}
                  onChange={(e) => handleInputChange("weight", e.target.value)}
                />
              </NumberInput>
            </FormControl>

            <FormControl>
              <FormLabel>Height (cm)</FormLabel>
              <NumberInput min={0} precision={1}>
                <NumberInputField
                  value={formData.height}
                  onChange={(e) => handleInputChange("height", e.target.value)}
                />
              </NumberInput>
            </FormControl>
          </VStack>
        </Box>

        {/* Symptoms */}
        <Box 
          w="100%" 
          p={6} 
          borderWidth={1} 
          borderRadius="lg" 
          shadow="sm"
          bg="white"
          borderColor="purple.200"
        >
          <VStack spacing={4}>
            <Heading size="md" color="purple.500">Current Symptoms</Heading>
            <FormControl>
              <FormLabel>Description</FormLabel>
              <Input
                value={formData.symptoms[0].description}
                onChange={(e) => handleSymptomChange("description", e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Date</FormLabel>
              <Input
                type="date"
                value={formData.symptoms[0].date}
                onChange={(e) => handleSymptomChange("date", e.target.value)}
              />
            </FormControl>
          </VStack>
        </Box>

        {/* Past Diagnosis */}
        <Box 
          w="100%" 
          p={6} 
          borderWidth={1} 
          borderRadius="lg" 
          shadow="sm"
          bg="white"
          borderColor="blue.200"
        >
          <VStack spacing={4}>
            <Heading size="md" color="blue.500">Past Diagnosis</Heading>
            <FormControl>
              <FormLabel>Diagnosis Name</FormLabel>
              <Input
                value={formData.past_diagnoses[0].name}
                onChange={(e) => handleDiagnosisChange("name", e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Description</FormLabel>
              <Input
                value={formData.past_diagnoses[0].description}
                onChange={(e) => handleDiagnosisChange("description", e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Doctor Name</FormLabel>
              <Input
                value={formData.past_diagnoses[0].doctor_name}
                onChange={(e) => handleDiagnosisChange("doctor_name", e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Date</FormLabel>
              <Input
                type="date"
                value={formData.past_diagnoses[0].date}
                onChange={(e) => handleDiagnosisChange("date", e.target.value)}
              />
            </FormControl>
          </VStack>
        </Box>

        <Button 
          type="submit" 
          colorScheme="teal" 
          size="lg"
          _hover={{ bg: "teal.500" }}
          _active={{ bg: "teal.600" }}
          boxShadow="md"
        >
          Add Patient
        </Button>
      </VStack>
    </Container>
  );
}
