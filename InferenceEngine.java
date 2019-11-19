import java.util.*;

public class InferenceEngine{
	
	public static void main(String args[]){
		Kattio io = new Kattio(System.in, System.out);
		ArrayList<Integer> predictions = new ArrayList<>();
		while(io.hasMoreTokens()){
			int nextDay = io.getInt();
			predictions.add(nextDay);
		}

	}

}
