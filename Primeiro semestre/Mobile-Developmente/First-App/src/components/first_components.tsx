import { View, Text, StyleSheet } from "react-native"
import { StatusBar } from "expo-status-bar"

interface Props {
  name: string;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export const FirtComponents = ({name}:Props) => {

    return(
    <View style={styles.container}>
      <Text>Muito complicado para fazer pouca coisa</Text>
      <StatusBar style="auto" />
    </View>
    )
}