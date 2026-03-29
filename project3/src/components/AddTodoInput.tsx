import React, { useState, useCallback } from 'react';
import { View, TextInput, TouchableOpacity, Text } from 'react-native';
import { useTodoStore } from '../store/useTodoStore';
import { triggerHaptic } from '../utils/haptics';

export const AddTodoInput = () => {
  const [text, setText] = useState('');
  const addTodo = useTodoStore((state) => state.addTodo);

  const handleAdd = useCallback(() => {
    if (text.trim()) {
      addTodo(text);
      setText('');
      triggerHaptic('success');
    }
  }, [text, addTodo]);

  return (
    <View className="flex-row p-4 gap-2">
      <TextInput 
        className="flex-1 bg-gray-100 p-3 rounded-lg" 
        value={text} 
        onChangeText={setText} 
        placeholder="Add a task..." 
      />
      <TouchableOpacity onPress={handleAdd} className="bg-blue-500 p-3 rounded-lg">
        <Text className="text-white font-bold">Add</Text>
      </TouchableOpacity>
    </View>
  );
};