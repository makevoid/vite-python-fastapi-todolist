import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@chakra-ui/react";
import TodoService from "../services/TodoService.js";

/**
 * Custom toast function with enhanced styling
 */
const createStyledToast =
  (toast) =>
  ({ title, description, status, duration = 3000, isClosable = true }) => {
    return toast({
      title,
      description,
      status,
      duration,
      isClosable,
      position: "top-right",
      variant: "subtle",
      containerStyle: {
        bg: "white",
        border: "1px solid",
        borderColor: status === "success" ? "green.200" : status === "error" ? "red.200" : "blue.200",
        borderRadius: "lg",
        boxShadow: "lg",
        color: "gray.800",
      },
    });
  };

/**
 * Custom hook for todo operations with React Query integration
 */
const useTodos = () => {
  const queryClient = useQueryClient();
  const toast = useToast();
  const styledToast = createStyledToast(toast);
  const todoService = new TodoService();

  // Query for fetching all todos
  const todosQuery = useQuery({
    queryKey: ["todos"],
    queryFn: () => todoService.fetchTodos(),
  });

  // Mutation for creating a todo
  const createTodoMutation = useMutation({
    mutationFn: ({ title, description }) => todoService.createTodo(title, description),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      styledToast({
        title: "Todo created",
        description: "Todo created successfully",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    },
  });

  // Mutation for updating a todo
  const updateTodoMutation = useMutation({
    mutationFn: ({ id, updates }) => todoService.updateTodo(id, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    },
  });

  // Mutation for toggling todo completion
  const toggleCompletionMutation = useMutation({
    mutationFn: (id) => todoService.toggleTodoCompletion(id),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      styledToast({
        title: data.completed ? "Todo completed" : "Todo uncompleted",
        description: `"${data.title}" marked as ${data.completed ? "completed" : "incomplete"}`,
        status: "info",
        duration: 2000,
        isClosable: true,
      });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    },
  });

  // Mutation for deleting a todo
  const deleteTodoMutation = useMutation({
    mutationFn: (id) => todoService.deleteTodo(id),
    onSuccess: (_, deletedId) => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      styledToast({
        title: "Todo deleted",
        description: "Todo deleted successfully",
        status: "info",
        duration: 3000,
        isClosable: true,
      });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    },
  });

  return {
    // Data
    todos: todosQuery.data || [],
    isLoading: todosQuery.isLoading,
    error: todosQuery.error,

    // Mutations
    createTodo: createTodoMutation.mutate,
    updateTodo: updateTodoMutation.mutate,
    toggleTodoCompletion: toggleCompletionMutation.mutate,
    deleteTodo: deleteTodoMutation.mutate,

    // Mutation states
    isCreating: createTodoMutation.isPending,
    isUpdating: updateTodoMutation.isPending,
    isToggling: toggleCompletionMutation.isPending,
    isDeleting: deleteTodoMutation.isPending,
  };
};

export default useTodos;
