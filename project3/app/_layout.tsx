import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <Stack screenOptions={{ headerTitle: 'Modern Tasks 2026' }} />
      <StatusBar style="auto" />
    </>
  );
}