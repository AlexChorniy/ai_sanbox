import React, { useCallback } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Todo, useTodoStore } from '../store/useTodoStore';
import { triggerHaptic } from '../utils/haptics';

// Wrapped in React.memo to prevent unnecessary re-renders in FlatList
export const TodoItem = React.memo(({ todo }: { todo: Todo }) => {
  const { toggleTodo, deleteTodo } = useTodoStore();

  const handleToggle = useCallback(() => {
    toggleTodo(todo.id);
    triggerHaptic('light');
  }, [todo.id, toggleTodo]);

  const handleDelete = useCallback(() => {
    deleteTodo(todo.id);
    triggerHaptic('heavy');
  }, [todo.id, deleteTodo]);

  return (
    <View className="flex-row items-center justify-between p-4 border-b border-gray-200">
      <TouchableOpacity onPress={handleToggle}>
        <Text className={todo.completed ? "line-through text-gray-400" : "text-black"}>
          {todo.text}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={handleDelete}>
        <Text className="text-red-500">Delete</Text>
      </TouchableOpacity>
    </View>
  );
});