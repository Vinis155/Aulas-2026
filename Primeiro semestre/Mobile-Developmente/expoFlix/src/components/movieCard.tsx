import { Movie } from "@/types/movie.type";
import { View, Text, StyleSheet, Image } from "react-native";

//AQUI TEMOS UMA PROP CHAMADA 'item' DO TIPO 'Movie'. O 'Movie' É UM ARQUIVO QUE ESTA DENTRO DA PASTA TYPES.
type Props = {
  item: Movie;
};

//COMPLETE OS VALORES DO OBJETO PARA QUE FUNCINE.
export const MovieCard = ({ item }: Props) => {
  return (
    <View style={styles.card}>
      <Image source={{ uri: item.poster }} style={styles.image} resizeMode="contain" />
      <View>
        <Text style={styles.titleMovie}>{item.title}</Text>
        <Text style={styles.description}>{item.description}</Text>
        <Text style={styles.text}>Lang: {item.language}</Text>
        <View style={styles.rank}>
          <Text style={styles.text}>Rank:</Text>
          <Text style={{ color: "yellow" }}>{item.rank}</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    width: "100%",
    backgroundColor: "#5C668B",
    marginBottom: 8,
    borderRadius: 8,
    padding: 8,
    flexDirection: "row",
    gap: 8,
  },
  titleMovie: {
    fontWeight: "500",
    fontSize: 16,
    color: "#fff",
  },
  description: {
    color: "#c5c5c5",
    fontSize: 12,
    marginBottom: 4,
  },
  text: {
    color: "#c5c5c5",
    fontSize: 12,
    marginBottom: 2,
  },
  containerCard: {
    flexDirection: "row",
    gap: 4,
  },
  image: {
    width: 80,
    height: 110,
  },
  rank: {
    flexDirection: "row",
    gap: 4,
  },
});
