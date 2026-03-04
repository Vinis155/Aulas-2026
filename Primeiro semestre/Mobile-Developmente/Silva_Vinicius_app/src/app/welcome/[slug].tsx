import { useLocalSearchParams } from "expo-router";
import { View, Text, StyleSheet } from "react-native";

export default function About() {

  /* O useLocalSearchParams é uma função do expo-router
     que recebe os parâmetros da URL */
  const { slug } = useLocalSearchParams<{ slug: string }>();

  return (
    <View style={styles.container}>
      
      {/* Tela simples mostrando o nome do usuário */}
      <Text>
        Olá, seja muito bem vindo ao React Native Expo!
      </Text>

      <Text>
        Parabéns, {slug}!
      </Text>

      <Text>
        Você concluiu o primeiro teste.
      </Text>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});