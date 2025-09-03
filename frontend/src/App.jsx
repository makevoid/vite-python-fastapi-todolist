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
  Textarea,
  Checkbox,
} from "@chakra-ui/react";
import { IoAdd, IoTrash, IoCheckmark, IoClose, IoCreate, IoLogoGithub } from "react-icons/io5";
import useTodos from "./hooks/useTodos.js";

function App() {
  const [newTodoTitle, setNewTodoTitle] = useState("");
  const [newTodoDescription, setNewTodoDescription] = useState("");
  const [editingTodo, setEditingTodo] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");

  const bgGradient = "linear(to-br, blue.50, gray.100, blue.100)";
  const cardBg = "white";
  const primaryColor = "blue.600";
  const headerBg = "white";
  const borderColor = "gray.200";

  // Use the custom hook for todo operations
  const {
    todos,
    isLoading,
    error,
    createTodo,
    updateTodo,
    toggleTodoCompletion,
    deleteTodo,
    isCreating,
    isUpdating,
    isToggling,
    isDeleting,
  } = useTodos();

  // Event handlers
  const handleCreateTodo = (e) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    createTodo({
      title: newTodoTitle,
      description: newTodoDescription,
    });

    setNewTodoTitle("");
    setNewTodoDescription("");
  };

  const handleToggleCompletion = (id) => {
    toggleTodoCompletion(id);
  };

  const handleDelete = (id) => {
    deleteTodo(id);
  };

  const handleStartEdit = (todo) => {
    setEditingTodo(todo.id);
    setEditTitle(todo.title);
    setEditDescription(todo.description);
  };

  const handleSaveEdit = () => {
    if (!editTitle.trim()) return;

    updateTodo({
      id: editingTodo,
      updates: {
        title: editTitle,
        description: editDescription,
      },
    });

    setEditingTodo(null);
    setEditTitle("");
    setEditDescription("");
  };

  const handleCancelEdit = () => {
    setEditingTodo(null);
    setEditTitle("");
    setEditDescription("");
  };

  const completedTodos = todos.filter((todo) => todo.completed);
  const pendingTodos = todos.filter((todo) => !todo.completed);

  if (error) {
    return (
      <Box minH="100vh" bgGradient={bgGradient} display="flex" alignItems="center" justifyContent="center">
        <Alert status="error" borderRadius="lg" maxW="md">
          <AlertIcon />
          <Box>
            <Text fontWeight="bold">Failed to load todos</Text>
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
                Todo List App
              </Heading>
              <Text color="gray.600" fontSize="sm" fontWeight="500">
                Manage Your Tasks
              </Text>
            </VStack>
            <Badge colorScheme="blue" variant="outline" px={3} py={1} borderRadius="full" fontWeight="600">
              Todo V1.0
            </Badge>
          </Flex>
        </Container>
      </Box>

      <Container maxW="7xl" py={8}>
        <VStack spacing={8}>
          {/* Create Todo Form */}
          <Card w="100%" bg={cardBg} shadow="sm" border="1px" borderColor={borderColor} borderRadius="lg">
            <CardHeader bg="gray.50" borderTopRadius="lg" borderBottom="1px" borderColor={borderColor}>
              <Flex align="center" gap={3}>
                <Box w={3} h={3} bg="blue.500" borderRadius="full" />
                <Heading size="md" color="gray.700" fontWeight="600">
                  Add New Todo
                </Heading>
              </Flex>
            </CardHeader>
            <CardBody p={6}>
              <form onSubmit={handleCreateTodo}>
                <VStack spacing={5}>
                  <Box w="100%">
                    <Text fontSize="sm" fontWeight="600" color="gray.700" mb={2}>
                      Todo Title
                    </Text>
                    <Input
                      placeholder="Enter todo title..."
                      value={newTodoTitle}
                      onChange={(e) => setNewTodoTitle(e.target.value)}
                      data-testid="todo-title-input"
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
                  <Box w="100%">
                    <Text fontSize="sm" fontWeight="600" color="gray.700" mb={2}>
                      Description (Optional)
                    </Text>
                    <Textarea
                      placeholder="Enter todo description..."
                      value={newTodoDescription}
                      onChange={(e) => setNewTodoDescription(e.target.value)}
                      data-testid="todo-description-input"
                      size="md"
                      borderRadius="md"
                      bg="white"
                      border="2px"
                      borderColor="gray.200"
                      focusBorderColor="blue.500"
                      _hover={{ borderColor: "gray.300" }}
                      color="gray.800"
                      _placeholder={{ color: "gray.400" }}
                      rows={3}
                    />
                  </Box>
                  <Button
                    type="submit"
                    colorScheme="blue"
                    size="md"
                    w="full"
                    data-testid="create-todo-btn"
                    borderRadius="md"
                    fontWeight="600"
                    px={8}
                    py={6}
                    _hover={{ transform: "translateY(-1px)", shadow: "md" }}
                    transition="all 0.2s"
                    isLoading={isCreating}
                    loadingText="Adding Todo..."
                    leftIcon={<IoAdd />}
                  >
                    Add Todo
                  </Button>
                </VStack>
              </form>
            </CardBody>
          </Card>

          {/* Todos List */}
          <Card w="100%" bg={cardBg} shadow="sm" border="1px" borderColor={borderColor} borderRadius="lg">
            <CardHeader bg="gray.50" borderTopRadius="lg" borderBottom="1px" borderColor={borderColor}>
              <Flex justify="space-between" align="center">
                <Flex align="center" gap={3}>
                  <Box w={3} h={3} bg="green.500" borderRadius="full" />
                  <Heading size="md" color="gray.700" fontWeight="600">
                    Your Todos
                  </Heading>
                </Flex>
                <HStack spacing={3}>
                  <Badge
                    colorScheme="orange"
                    variant="solid"
                    borderRadius="md"
                    px={3}
                    py={1}
                    fontWeight="600"
                  >
                    {pendingTodos.length} Pending
                  </Badge>
                  <Badge colorScheme="green" variant="solid" borderRadius="md" px={3} py={1} fontWeight="600">
                    {completedTodos.length} Done
                  </Badge>
                </HStack>
              </Flex>
            </CardHeader>
            <CardBody p={6}>
              {isLoading && (
                <Flex justify="center" p={12}>
                  <VStack spacing={4}>
                    <Spinner size="lg" color="blue.500" thickness="3px" />
                    <Text color="gray.600" fontSize="sm" fontWeight="500">
                      Loading todos...
                    </Text>
                  </VStack>
                </Flex>
              )}

              {!isLoading && todos.length === 0 && (
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
                      📝
                    </Box>
                    <VStack spacing={2}>
                      <Text color="gray.700" fontWeight="600" fontSize="lg">
                        No todos yet
                      </Text>
                      <Text color="gray.500" fontSize="sm">
                        Add your first todo using the form above to get started.
                      </Text>
                    </VStack>
                  </VStack>
                </Box>
              )}

              {!isLoading && todos.length > 0 && (
                <VStack spacing={4} align="stretch">
                  {todos.map((todo) => (
                    <Card
                      key={todo.id}
                      bg="white"
                      borderRadius="lg"
                      shadow="sm"
                      _hover={{ shadow: "md", borderColor: "blue.300" }}
                      transition="all 0.2s"
                      data-testid={`todo-${todo.id}`}
                      border="2px"
                      borderColor={todo.completed ? "green.200" : "gray.200"}
                      opacity={todo.completed ? 0.8 : 1}
                    >
                      <CardBody p={5}>
                        {editingTodo === todo.id ? (
                          <VStack spacing={4} align="stretch">
                            <Input
                              value={editTitle}
                              onChange={(e) => setEditTitle(e.target.value)}
                              data-testid={`edit-title-${todo.id}`}
                              size="md"
                              borderRadius="md"
                              fontWeight="600"
                              bg="white"
                              border="2px"
                              borderColor="blue.200"
                              color="gray.800"
                              focusBorderColor="blue.500"
                              _hover={{ borderColor: "blue.300" }}
                              _placeholder={{ color: "gray.400" }}
                            />
                            <Textarea
                              value={editDescription}
                              onChange={(e) => setEditDescription(e.target.value)}
                              data-testid={`edit-description-${todo.id}`}
                              size="md"
                              borderRadius="md"
                              rows={3}
                              bg="white"
                              border="2px"
                              borderColor="blue.200"
                              color="gray.800"
                              focusBorderColor="blue.500"
                              _hover={{ borderColor: "blue.300" }}
                              _placeholder={{ color: "gray.400" }}
                            />
                            <HStack spacing={2}>
                              <Button
                                colorScheme="blue"
                                size="sm"
                                onClick={handleSaveEdit}
                                data-testid={`save-edit-${todo.id}`}
                                leftIcon={<IoCheckmark />}
                                isLoading={isUpdating}
                              >
                                Save
                              </Button>
                              <Button
                                colorScheme="gray"
                                variant="outline"
                                size="sm"
                                onClick={handleCancelEdit}
                                data-testid={`cancel-edit-${todo.id}`}
                                leftIcon={<IoClose />}
                              >
                                Cancel
                              </Button>
                            </HStack>
                          </VStack>
                        ) : (
                          <VStack spacing={3} align="stretch">
                            <Flex align="flex-start" gap={3}>
                              <Checkbox
                                isChecked={todo.completed}
                                onChange={() => handleToggleCompletion(todo.id)}
                                data-testid={`toggle-${todo.id}`}
                                size="lg"
                                colorScheme="green"
                                mt={1}
                                isDisabled={isToggling}
                                borderColor="gray.400"
                                _hover={{
                                  borderColor: "green.400",
                                }}
                                _checked={{
                                  bg: "green.500",
                                  borderColor: "green.500",
                                  color: "white",
                                  _hover: {
                                    bg: "green.600",
                                    borderColor: "green.600",
                                  },
                                }}
                              />
                              <Box flex={1}>
                                <Text
                                  fontSize="lg"
                                  fontWeight="600"
                                  color={todo.completed ? "gray.500" : "gray.800"}
                                  textDecoration={todo.completed ? "line-through" : "none"}
                                  data-testid={`title-${todo.id}`}
                                >
                                  {todo.title}
                                </Text>
                                {todo.description && (
                                  <Text
                                    fontSize="sm"
                                    color={todo.completed ? "gray.400" : "gray.600"}
                                    mt={2}
                                    data-testid={`description-${todo.id}`}
                                  >
                                    {todo.description}
                                  </Text>
                                )}
                              </Box>
                              <HStack spacing={2}>
                                <IconButton
                                  icon={<IoCreate />}
                                  colorScheme="blue"
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleStartEdit(todo)}
                                  data-testid={`edit-${todo.id}`}
                                  aria-label="Edit todo"
                                />
                                <IconButton
                                  icon={<IoTrash />}
                                  colorScheme="red"
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleDelete(todo.id)}
                                  data-testid={`delete-${todo.id}`}
                                  isLoading={isDeleting}
                                  aria-label="Delete todo"
                                />
                              </HStack>
                            </Flex>
                          </VStack>
                        )}
                      </CardBody>
                    </Card>
                  ))}
                </VStack>
              )}
            </CardBody>
          </Card>
        </VStack>
      </Container>

      {/* Footer */}
      <Box bg={headerBg} borderTop="1px" borderColor={borderColor} py={6} mt={8}>
        <Container maxW="7xl">
          <Flex justify="center" align="center" gap={3}>
            <IoLogoGithub size={24} color="gray.600" />
            <Text fontSize="sm" color="gray.600">
              View source code on{" "}
              <Text
                as="a"
                href="https://github.com/makevoid/vite-python-fastapi-todolist"
                rel="noopener noreferrer"
                color={primaryColor}
                fontWeight="600"
                _hover={{ textDecoration: "underline" }}
              >
                GitHub
              </Text>
            </Text>
          </Flex>
        </Container>
      </Box>
    </Box>
  );
}

export default App;
