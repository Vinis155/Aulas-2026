import { useRouter } from "expo-router";
import { View, Text,Button } from "react-native"


export default function FirstScream() {
    const router = useRouter();

    return(
        <View>
            <Text>Primeira tela</Text>
            <Button title="Ir para a segunda tela" onPress={() => router.push('/secondScream')} />
        </View>
    )
}