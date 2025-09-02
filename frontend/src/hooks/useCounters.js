import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@chakra-ui/react";
import CounterService from "../services/CounterService.js";

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
 * Custom hook for counter operations with React Query integration
 */
const useCounters = () => {
  const queryClient = useQueryClient();
  const toast = useToast();
  const styledToast = createStyledToast(toast);
  const counterService = new CounterService();

  // Query for fetching all counters
  const countersQuery = useQuery({
    queryKey: ["counters"],
    queryFn: () => counterService.fetchCounters(),
  });

  // Mutation for creating a counter
  const createCounterMutation = useMutation({
    mutationFn: ({ name, initial_value }) => counterService.createCounter(name, initial_value),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["counters"] });
      styledToast({
        title: "Counter created",
        description: "Counter created successfully",
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

  // Mutation for incrementing a counter
  const incrementMutation = useMutation({
    mutationFn: ({ name, amount }) => counterService.incrementCounter(name, amount),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["counters"] });
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

  // Mutation for decrementing a counter
  const decrementMutation = useMutation({
    mutationFn: ({ name, amount }) => counterService.decrementCounter(name, amount),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["counters"] });
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

  // Mutation for resetting a counter
  const resetMutation = useMutation({
    mutationFn: (name) => counterService.resetCounter(name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["counters"] });
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

  // Mutation for updating a counter
  const updateMutation = useMutation({
    mutationFn: ({ name, value }) => counterService.updateCounter(name, value),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["counters"] });
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

  // Mutation for deleting a counter
  const deleteMutation = useMutation({
    mutationFn: (name) => counterService.deleteCounter(name),
    onSuccess: (_, deletedName) => {
      queryClient.invalidateQueries({ queryKey: ["counters"] });
      styledToast({
        title: "Counter deleted",
        description: `Counter "${deletedName}" deleted successfully`,
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
    counters: countersQuery.data || [],
    isLoading: countersQuery.isLoading,
    error: countersQuery.error,

    // Mutations
    createCounter: createCounterMutation.mutate,
    incrementCounter: incrementMutation.mutate,
    decrementCounter: decrementMutation.mutate,
    resetCounter: resetMutation.mutate,
    updateCounter: updateMutation.mutate,
    deleteCounter: deleteMutation.mutate,

    // Mutation states
    isCreating: createCounterMutation.isPending,
    isIncrementing: incrementMutation.isPending,
    isDecrementing: decrementMutation.isPending,
    isResetting: resetMutation.isPending,
    isUpdating: updateMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
};

export default useCounters;
