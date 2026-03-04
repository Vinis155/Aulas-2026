import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen 
        name="index" 
        options={{ title: "Home" }} 
      />
      
      <Stack.Screen 
        name="welcome/[slug]" 
        options={{ title: "Welcome" }} 
      />
    </Stack>
  );
}