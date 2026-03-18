import { useRouter } from "expo-router";
import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";

//AQUI COMPLETE O CSS DA TELA. DEIXE MINIMAMENTE PARECIDO COM A IMAGEM.
export default function Perfil() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.perfil}>Perfil</Text>
      <View style={styles.perfilContainer}>
        <Image
          style={styles.avatar}
          resizeMode="cover"
          source={require("../../../assets/images/punpun.jpg")}
        />
        <Text style={styles.text}>Nome: Punpun</Text>
        <Text style={styles.text}>Email: boanoite.punpun@gmail.com</Text>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.replace("/")}
        >
          <Text style={styles.btnTitle}>Sair</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#19244B",
    justifyContent: "center",
    alignItems: "center",
    padding: 16,
  },
  perfil: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 40,
  },
  perfilContainer: {
    alignItems: "center",
    backgroundColor: "rgba(255, 255, 255, 0.05)",
    padding: 24,
    borderRadius: 12,
    width: "100%",
    maxWidth: 300,
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 20,
    borderWidth: 3,
    borderColor: "#fff",
  },
  text: {
    color: "#fff",
    fontSize: 16,
    marginBottom: 12,
    textAlign: "center",
  },
  button: {
    backgroundColor: "#fff",
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 8,
    marginTop: 24,
    width: "100%",
  },
  btnTitle: {
    color: "#19244B",
    fontWeight: "bold",
    fontSize: 16,
    textAlign: "center",
  },
});
