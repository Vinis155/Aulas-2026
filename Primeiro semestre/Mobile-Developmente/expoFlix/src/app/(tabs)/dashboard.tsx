import { MovieCard } from "@/components/movieCard";
import { Movies } from "@/services/movie";
import { StatusBar } from "expo-status-bar";
import { FlatList, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

//NOTE QUE TEMOS UMA TAG NOVA CHAMADA 'FlatList'. ESSA TAG RENDERIZA NOSSAS LISTAS.
//IMPORTE A LISTA 'Movies' PARA QUE FUNCIONE CORRETAMENTE.
//CRIE A LISTA 'Movies' ESTA DENTRO DA PASTA SERVICES.
export default function Dashboard() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Filmes</Text>
      <FlatList
        data={Movies}
        renderItem={({ item }) => <MovieCard item={item} />}
        keyExtractor={(item) => item.id}
      />
      <StatusBar style="auto" hidden />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#19244B",
    padding: 8,
  },
  title: {
    color: "white",
    fontSize: 20,
    marginBottom: 30,
  },
});
