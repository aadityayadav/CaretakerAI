"use client";
import { useState, useEffect, useRef } from "react";
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
  HStack,
  IconButton,
} from "@chakra-ui/react";
import { AddIcon, DeleteIcon, ChevronDownIcon } from '@chakra-ui/icons';

interface MedicalCondition {
  description: string;
  date: string;
  id: number;
}

interface PastDiagnosis {
  name: string;
  description: string;
  doctor_name: string;
  date: string;
  id: number;
}

interface Medication {
  name: string;
  dosage: string;
  frequency: string;
  date: string;
  id: number;
}

interface Allergy {
  name: string;
  severity: string;
  date: string;
  id: number;
}

export default function AddPatient() {
  const toast = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    age: "",
    gender: "",
    weight: "",
    height: "",
    medical_conditions: [] as MedicalCondition[],
    past_diagnoses: [] as PastDiagnosis[],
    allergies: [] as Allergy[],
    medications: [] as Medication[],
  });

  const bottomRef = useRef<HTMLDivElement>(null);
  const sectionRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const scrollToNewSection = (type: string, id: number) => {
    // Small delay to ensure the new section is rendered
    setTimeout(() => {
      sectionRefs.current[`${type}-${id}`]?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const addMedicalCondition = () => {
    const newId = formData.medical_conditions.length + 1;
    setFormData(prev => ({
      ...prev,
      medical_conditions: [
        ...prev.medical_conditions,
        {
          description: "",
          date: new Date().toISOString().split('T')[0],
          id: newId
        }
      ]
    }));
    scrollToNewSection('medical_conditions', newId);
  };

  const addPastDiagnosis = () => {
    const newId = formData.past_diagnoses.length + 1;
    setFormData(prev => ({
      ...prev,
      past_diagnoses: [
        ...prev.past_diagnoses,
        {
          name: "",
          description: "",
          doctor_name: "",
          date: new Date().toISOString().split('T')[0],
          id: newId
        }
      ]
    }));
    scrollToNewSection('past_diagnoses', newId);
  };

  const addMedication = () => {
    const newId = formData.medications.length + 1;
    setFormData(prev => ({
      ...prev,
      medications: [
        ...prev.medications,
        {
          name: "",
          dosage: "",
          frequency: "",
          date: new Date().toISOString().split('T')[0],
          id: newId
        }
      ]
    }));
    scrollToNewSection('medications', newId);
  };

  const addAllergy = () => {
    const newId = formData.allergies.length + 1;
    setFormData(prev => ({
      ...prev,
      allergies: [
        ...prev.allergies,
        {
          name: "",
          severity: "",
          date: new Date().toISOString().split('T')[0],
          id: newId
        }
      ]
    }));
    scrollToNewSection('allergies', newId);
  };

  const handleMedicalConditionChange = (id: number, field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      medical_conditions: prev.medical_conditions.map(condition =>
        condition.id === id ? { ...condition, [field]: value } : condition
      )
    }));
  };

  const handlePastDiagnosisChange = (id: number, field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      past_diagnoses: prev.past_diagnoses.map(diagnosis =>
        diagnosis.id === id ? { ...diagnosis, [field]: value } : diagnosis
      )
    }));
  };

  const handleMedicationChange = (id: number, field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      medications: prev.medications.map(medication =>
        medication.id === id ? { ...medication, [field]: value } : medication
      )
    }));
  };

  const handleAllergyChange = (id: number, field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      allergies: prev.allergies.map(allergy =>
        allergy.id === id ? { ...allergy, [field]: value } : allergy
      )
    }));
  };

  const removeItem = (type: string, id: number) => {
    setFormData(prev => ({
      ...prev,
      [type]: prev[type]
        .filter(item => item.id !== id)
        .map((item, index) => ({
          ...item,
          id: index + 1
        }))
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

  const renderSectionHeader = (type: string, id: number, title: string, color: string) => (
    <Box w="100%" position="relative" h="40px">
      <IconButton
        aria-label="Scroll to bottom"
        icon={<ChevronDownIcon />}
        onClick={scrollToBottom}
        colorScheme={color}
        size="sm"
        position="absolute"
        left="0"
      />
      <Heading 
        size="md" 
        color={`${color}.500`}
        position="absolute"
        left="50%"
        transform="translateX(-50%)"
      >
        {title} #{id}
      </Heading>
      <IconButton
        aria-label={`Remove ${title.toLowerCase()}`}
        icon={<DeleteIcon />}
        onClick={() => removeItem(type, id)}
        colorScheme="red"
        size="sm"
        position="absolute"
        right="0"
      />
    </Box>
  );

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

        {/* Medical Conditions */}
        {formData.medical_conditions.map((condition) => (
          <Box 
            key={condition.id}
            ref={el => sectionRefs.current[`medical_conditions-${condition.id}`] = el}
            w="100%" 
            p={6} 
            borderWidth={1} 
            borderRadius="lg" 
            shadow="sm"
            bg="white"
            borderColor="purple.200"
          >
            <VStack spacing={4}>
              {renderSectionHeader('medical_conditions', condition.id, 'Medical Condition', 'purple')}
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Input
                  value={condition.description}
                  onChange={(e) => handleMedicalConditionChange(condition.id, "description", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Date</FormLabel>
                <Input
                  type="date"
                  value={condition.date}
                  onChange={(e) => handleMedicalConditionChange(condition.id, "date", e.target.value)}
                />
              </FormControl>
            </VStack>
          </Box>
        ))}

        {/* Past Diagnoses */}
        {formData.past_diagnoses.map((diagnosis) => (
          <Box 
            key={diagnosis.id}
            ref={el => sectionRefs.current[`past_diagnoses-${diagnosis.id}`] = el}
            w="100%" 
            p={6} 
            borderWidth={1} 
            borderRadius="lg" 
            shadow="sm"
            bg="white"
            borderColor="blue.200"
          >
            <VStack spacing={4}>
              {renderSectionHeader('past_diagnoses', diagnosis.id, 'Past Diagnosis', 'blue')}
              <FormControl>
                <FormLabel>Diagnosis Name</FormLabel>
                <Input
                  value={diagnosis.name}
                  onChange={(e) => handlePastDiagnosisChange(diagnosis.id, "name", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Input
                  value={diagnosis.description}
                  onChange={(e) => handlePastDiagnosisChange(diagnosis.id, "description", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Doctor Name</FormLabel>
                <Input
                  value={diagnosis.doctor_name}
                  onChange={(e) => handlePastDiagnosisChange(diagnosis.id, "doctor_name", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Date</FormLabel>
                <Input
                  type="date"
                  value={diagnosis.date}
                  onChange={(e) => handlePastDiagnosisChange(diagnosis.id, "date", e.target.value)}
                />
              </FormControl>
            </VStack>
          </Box>
        ))}

        {/* Medications */}
        {formData.medications.map((medication) => (
          <Box 
            key={medication.id}
            ref={el => sectionRefs.current[`medications-${medication.id}`] = el}
            w="100%" 
            p={6} 
            borderWidth={1} 
            borderRadius="lg" 
            shadow="sm"
            bg="white"
            borderColor="green.200"
          >
            <VStack spacing={4}>
              {renderSectionHeader('medications', medication.id, 'Medication', 'green')}
              <FormControl>
                <FormLabel>Medication Name</FormLabel>
                <Input
                  value={medication.name}
                  onChange={(e) => handleMedicationChange(medication.id, "name", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Dosage</FormLabel>
                <Input
                  value={medication.dosage}
                  onChange={(e) => handleMedicationChange(medication.id, "dosage", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Frequency</FormLabel>
                <Input
                  value={medication.frequency}
                  onChange={(e) => handleMedicationChange(medication.id, "frequency", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Date</FormLabel>
                <Input
                  type="date"
                  value={medication.date}
                  onChange={(e) => handleMedicationChange(medication.id, "date", e.target.value)}
                />
              </FormControl>
            </VStack>
          </Box>
        ))}

        {/* Allergies */}
        {formData.allergies.map((allergy) => (
          <Box 
            key={allergy.id}
            ref={el => sectionRefs.current[`allergies-${allergy.id}`] = el}
            w="100%" 
            p={6} 
            borderWidth={1} 
            borderRadius="lg" 
            shadow="sm"
            bg="white"
            borderColor="orange.200"
          >
            <VStack spacing={4}>
              {renderSectionHeader('allergies', allergy.id, 'Allergy', 'orange')}
              <FormControl>
                <FormLabel>Allergy Name</FormLabel>
                <Input
                  value={allergy.name}
                  onChange={(e) => handleAllergyChange(allergy.id, "name", e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Severity</FormLabel>
                <Select
                  value={allergy.severity}
                  onChange={(e) => handleAllergyChange(allergy.id, "severity", e.target.value)}
                >
                  <option value="mild">Mild</option>
                  <option value="moderate">Moderate</option>
                  <option value="severe">Severe</option>
                </Select>
              </FormControl>
              <FormControl>
                <FormLabel>Date Discovered</FormLabel>
                <Input
                  type="date"
                  value={allergy.date}
                  onChange={(e) => handleAllergyChange(allergy.id, "date", e.target.value)}
                />
              </FormControl>
            </VStack>
          </Box>
        ))}

        {/* Add Buttons */}
        <div ref={bottomRef}>
          <HStack spacing={4} w="100%" justify="center">
            <Button
              leftIcon={<AddIcon />}
              onClick={addMedicalCondition}
              colorScheme="purple"
            >
              Add Medical Condition
            </Button>
            <Button
              leftIcon={<AddIcon />}
              onClick={addPastDiagnosis}
              colorScheme="blue"
            >
              Add Past Diagnosis
            </Button>
            <Button
              leftIcon={<AddIcon />}
              onClick={addMedication}
              colorScheme="green"
            >
              Add Medication
            </Button>
            <Button
              leftIcon={<AddIcon />}
              onClick={addAllergy}
              colorScheme="orange"
            >
              Add Allergy
            </Button>
          </HStack>
        </div>

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
