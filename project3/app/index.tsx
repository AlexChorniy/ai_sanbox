import React, { useCallback } from "react";
import { SafeAreaView, FlatList } from "react-native";
import { useTodoStore, Todo } from "../src/store/useTodoStore";
import { AddTodoInput } from "../src/components/AddTodoInput";
import { TodoItem } from "../src/components/TodoItem";

export default function TodoScreen() {
  const todos = useTodoStore((state) => state.todos);

  // Extracted renderItem to prevent inline function recreation on every render
  const renderItem = useCallback(
    ({ item }: { item: Todo }) => <TodoItem todo={item} />,
    [],
  );

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <AddTodoInput />
      <FlatList
        data={todos}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        // Performance optimizations for FlatList
        initialNumToRender={10}
        maxToRenderPerBatch={10}
        windowSize={5}
        removeClippedSubviews={true}
      />
    </SafeAreaView>
  );
}
