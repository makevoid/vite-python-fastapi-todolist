import React, { useState } from "react";
import {
  Box,
  Container,
  Heading,
  VStack,
  HStack,
  Button,
  Input,
  Text,
  Spinner,
  Flex,
  IconButton,
  Alert,
  AlertIcon,
  Badge,
  Divider,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
} from "@chakra-ui/react";
import { IoAdd, IoRemove, IoRefresh, IoTrash } from "react-icons/io5";
import useCounters from "./hooks/useCounters.js";

function App() {
  const [newCounterName, setNewCounterName] = useState("");
  const [newCounterValue, setNewCounterValue] = useState(0);

  const bgGradient = "linear(to-br, blue.50, gray.100, blue.100)";
  const cardBg = "white";
  const counterBg = "gray.50";
  const primaryColor = "blue.600";
  const headerBg = "white";
  const borderColor = "gray.200";

  // Use the custom hook for counter operations
  const {
    counters,
    isLoading,
    error,
    createCounter,
    incrementCounter,
    decrementCounter,
    resetCounter,
    updateCounter,
    deleteCounter,
    isCreating,
    isIncrementing,
    isDecrementing,
    isResetting,
    isUpdating,
    isDeleting,
  } = useCounters();

  // Event handlers
  const handleCreateCounter = (e) => {
    e.preventDefault();
    if (!newCounterName.trim()) return;

    createCounter({
      name: newCounterName,
      initial_value: parseInt(newCounterValue) || 0,
    });

    setNewCounterName("");
    setNewCounterValue(0);
  };

  const handleIncrement = (name, amount = 1) => {
    incrementCounter({ name, amount });
  };

  const handleDecrement = (name, amount = 1) => {
    decrementCounter({ name, amount });
  };

  const handleReset = (name) => {
    resetCounter(name);
  };

  const handleUpdate = (name, value) => {
    updateCounter({ name, value });
  };

  const handleDelete = (name) => {
    deleteCounter(name);
  };

  if (error) {
    return (
      <Box minH="100vh" bgGradient={bgGradient} display="flex" alignItems="center" justifyContent="center">
        <Alert status="error" borderRadius="lg" maxW="md">
          <AlertIcon />
          <Box>
            <Text fontWeight="bold">Failed to load counters</Text>
            <Text>{error.message}</Text>
          </Box>
        </Alert>
      </Box>
    );
  }

  return (
    <Box minH="100vh" bgGradient={bgGradient}>
      {/* Business Header */}
      <Box bg={headerBg} borderBottom="1px" borderColor={borderColor} shadow="sm">
        <Container maxW="7xl" py={4}>
          <Flex justify="space-between" align="center">
            <VStack align="start" spacing={1}>
              <Heading as="h1" size="xl" color={primaryColor} fontWeight="600" letterSpacing="-0.5px">
                Counter App
              </Heading>
              <Text color="gray.600" fontSize="sm" fontWeight="500">
                Dashboard
              </Text>
            </VStack>
            <Badge colorScheme="blue" variant="outline" px={3} py={1} borderRadius="full" fontWeight="600">
              Counter V1.0
            </Badge>
          </Flex>
        </Container>
      </Box>

      <Container maxW="7xl" py={8}>
        <VStack spacing={8}>
          {/* Create Counter Form */}
          <Card w="100%" bg={cardBg} shadow="sm" border="1px" borderColor={borderColor} borderRadius="lg">
            <CardHeader bg="gray.50" borderTopRadius="lg" borderBottom="1px" borderColor={borderColor}>
              <Flex align="center" gap={3}>
                <Box w={3} h={3} bg="blue.500" borderRadius="full" />
                <Heading size="md" color="gray.700" fontWeight="600">
                  Create New Counter
                </Heading>
              </Flex>
            </CardHeader>
            <CardBody p={6}>
              <form onSubmit={handleCreateCounter}>
                <VStack spacing={5}>
                  <HStack w="100%" spacing={4}>
                    <Box flex={2}>
                      <Text fontSize="sm" fontWeight="600" color="gray.700" mb={2}>
                        Counter Name
                      </Text>
                      <Input
                        placeholder="Enter counter name..."
                        value={newCounterName}
                        onChange={(e) => setNewCounterName(e.target.value)}
                        data-testid="counter-name-input"
                        size="md"
                        borderRadius="md"
                        bg="white"
                        border="2px"
                        borderColor="gray.200"
                        focusBorderColor="blue.500"
                        _hover={{ borderColor: "gray.300" }}
                        color="gray.800"
                        _placeholder={{ color: "gray.400" }}
                      />
                    </Box>
                    <Box flex={1}>
                      <Text fontSize="sm" fontWeight="600" color="gray.700" mb={2}>
                        Initial Value
                      </Text>
                      <Input
                        type="number"
                        value={newCounterValue}
                        onChange={(e) => setNewCounterValue(e.target.value)}
                        placeholder="0"
                        data-testid="counter-value-input"
                        size="md"
                        borderRadius="md"
                        bg="white"
                        border="2px"
                        borderColor="gray.200"
                        min={-999999}
                        max={999999}
                        focusBorderColor="blue.500"
                        _hover={{ borderColor: "gray.300" }}
                        color="gray.800"
                        _placeholder={{ color: "gray.400" }}
                      />
                    </Box>
                  </HStack>
                  <Button
                    type="submit"
                    colorScheme="blue"
                    size="md"
                    w="full"
                    data-testid="create-counter-btn"
                    borderRadius="md"
                    fontWeight="600"
                    px={8}
                    py={6}
                    _hover={{ transform: "translateY(-1px)", shadow: "md" }}
                    transition="all 0.2s"
                    isLoading={isCreating}
                    loadingText="Creating Counter..."
                  >
                    Create Counter
                  </Button>
                </VStack>
              </form>
            </CardBody>
          </Card>

          {/* Counters List */}
          <Card w="100%" bg={cardBg} shadow="sm" border="1px" borderColor={borderColor} borderRadius="lg">
            <CardHeader bg="gray.50" borderTopRadius="lg" borderBottom="1px" borderColor={borderColor}>
              <Flex justify="space-between" align="center">
                <Flex align="center" gap={3}>
                  <Box w={3} h={3} bg="green.500" borderRadius="full" />
                  <Heading size="md" color="gray.700" fontWeight="600">
                    Active Counters
                  </Heading>
                </Flex>
                {counters.length > 0 && (
                  <Badge colorScheme="blue" variant="solid" borderRadius="md" px={3} py={1} fontWeight="600">
                    {counters.length} Active
                  </Badge>
                )}
              </Flex>
            </CardHeader>
            <CardBody p={6}>
              {isLoading && (
                <Flex justify="center" p={12}>
                  <VStack spacing={4}>
                    <Spinner size="lg" color="blue.500" thickness="3px" />
                    <Text color="gray.600" fontSize="sm" fontWeight="500">
                      Loading counters...
                    </Text>
                  </VStack>
                </Flex>
              )}

              {!isLoading && counters.length === 0 && (
                <Box
                  textAlign="center"
                  p={12}
                  bg="gray.50"
                  border="2px dashed"
                  borderColor="gray.300"
                  borderRadius="lg"
                >
                  <VStack spacing={4}>
                    <Box fontSize="4xl" color="gray.400">
                      📊
                    </Box>
                    <VStack spacing={2}>
                      <Text color="gray.700" fontWeight="600" fontSize="lg">
                        No counters configured
                      </Text>
                      <Text color="gray.500" fontSize="sm">
                        Create your first counter using the form above to get started.
                      </Text>
                    </VStack>
                  </VStack>
                </Box>
              )}

              {!isLoading && counters.length > 0 && (
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={5}>
                  {counters.map((counter) => (
                    <Card
                      key={counter.id}
                      bg="white"
                      borderRadius="lg"
                      shadow="sm"
                      _hover={{ shadow: "md", borderColor: "blue.300" }}
                      transition="all 0.2s"
                      data-testid={`counter-${counter.name}`}
                      border="2px"
                      borderColor="gray.200"
                    >
                      <CardBody p={5}>
                        <VStack spacing={4}>
                          <Box
                            w="full"
                            bg="gray.50"
                            p={3}
                            borderRadius="md"
                            border="1px"
                            borderColor="gray.200"
                          >
                            <Text fontSize="sm" fontWeight="600" color="gray.600" textAlign="center" mb={1}>
                              COUNTER ID
                            </Text>
                            <Text
                              fontSize="md"
                              fontWeight="700"
                              color="gray.800"
                              textAlign="center"
                              noOfLines={1}
                            >
                              {counter.name}
                            </Text>
                          </Box>

                          <Box textAlign="center" py={4}>
                            <Text fontSize="xs" fontWeight="600" color="gray.500" mb={2}>
                              CURRENT VALUE
                            </Text>
                            <Text
                              fontSize="4xl"
                              fontWeight="800"
                              color="blue.600"
                              fontFamily="mono"
                              data-testid={`value-${counter.name}`}
                              lineHeight={1}
                            >
                              {counter.value}
                            </Text>
                          </Box>

                          <Box w="full" h="1px" bg="gray.200" />

                          {/* Counter Controls */}
                          <VStack spacing={3} w="100%">
                            <Text fontSize="xs" fontWeight="600" color="gray.500" textAlign="center">
                              OPERATIONS
                            </Text>
                            <HStack spacing={2} justify="center" w="full">
                              <Button
                                leftIcon={<IoRemove />}
                                colorScheme="red"
                                variant="outline"
                                size="sm"
                                onClick={() => handleDecrement(counter.name, 10)}
                                data-testid={`decrement-10-${counter.name}`}
                                borderRadius="md"
                                fontSize="xs"
                                fontWeight="600"
                                isLoading={isDecrementing}
                                flex={1}
                              >
                                -10
                              </Button>
                              <Button
                                colorScheme="red"
                                variant="outline"
                                size="sm"
                                onClick={() => handleDecrement(counter.name)}
                                data-testid={`decrement-${counter.name}`}
                                borderRadius="md"
                                fontSize="xs"
                                fontWeight="600"
                                isLoading={isDecrementing}
                                flex={1}
                              >
                                -1
                              </Button>
                              <Button
                                leftIcon={<IoRefresh />}
                                colorScheme="gray"
                                variant="outline"
                                size="sm"
                                onClick={() => handleReset(counter.name)}
                                data-testid={`reset-${counter.name}`}
                                borderRadius="md"
                                fontSize="xs"
                                fontWeight="600"
                                isLoading={isResetting}
                                flex={1}
                              >
                                RST
                              </Button>
                              <Button
                                colorScheme="green"
                                variant="outline"
                                size="sm"
                                onClick={() => handleIncrement(counter.name)}
                                data-testid={`increment-${counter.name}`}
                                borderRadius="md"
                                fontSize="xs"
                                fontWeight="600"
                                isLoading={isIncrementing}
                                flex={1}
                              >
                                +1
                              </Button>
                              <Button
                                leftIcon={<IoAdd />}
                                colorScheme="green"
                                variant="outline"
                                size="sm"
                                onClick={() => handleIncrement(counter.name, 10)}
                                data-testid={`increment-10-${counter.name}`}
                                borderRadius="md"
                                fontSize="xs"
                                fontWeight="600"
                                isLoading={isIncrementing}
                                flex={1}
                              >
                                +10
                              </Button>
                            </HStack>

                            {/* Counter Actions */}
                            <VStack w="100%" spacing={2}>
                              <Text fontSize="xs" fontWeight="600" color="gray.500" textAlign="center">
                                DIRECT SET
                              </Text>
                              <HStack w="100%" spacing={2}>
                                <Input
                                  type="number"
                                  placeholder="Enter value"
                                  data-testid={`set-value-${counter.name}`}
                                  size="sm"
                                  borderRadius="md"
                                  flex={1}
                                  bg="white"
                                  border="2px"
                                  borderColor="gray.200"
                                  fontSize="xs"
                                  fontWeight="600"
                                  _hover={{ borderColor: "gray.300" }}
                                  _focus={{ borderColor: "blue.400" }}
                                  color="gray.800"
                                  _placeholder={{ color: "gray.400" }}
                                  onKeyPress={(e) => {
                                    if (e.key === "Enter") {
                                      handleUpdate(counter.name, e.target.value);
                                      e.target.value = "";
                                    }
                                  }}
                                />
                                <Button
                                  leftIcon={<IoTrash />}
                                  colorScheme="red"
                                  variant="outline"
                                  size="sm"
                                  onClick={() => handleDelete(counter.name)}
                                  data-testid={`delete-${counter.name}`}
                                  borderRadius="md"
                                  fontSize="xs"
                                  fontWeight="600"
                                  isLoading={isDeleting}
                                >
                                  DEL
                                </Button>
                              </HStack>
                            </VStack>
                          </VStack>
                        </VStack>
                      </CardBody>
                    </Card>
                  ))}
                </SimpleGrid>
              )}
            </CardBody>
          </Card>
        </VStack>
      </Container>
    </Box>
  );
}

export default App;
