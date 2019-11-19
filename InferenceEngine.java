import java.util.*;

public class InferenceEngine{
	
	public static void main(String args[]){
		String separator = "END";
		Scanner in = new Scanner(System.in);
		ArrayList<Integer> LRPredictions = new ArrayList<>();
		ArrayList<Integer> SVRPredictions = new ArrayList<>();
		String c = in.nextLine();
		while(!c.equals(separator)){
			LRPredictions.add(Integer.parseInt(c));
			c = in.nextLine();
		}
		while(in.hasNext()){
			c = in.nextLine();
			SVRPredictions.add(Integer.parseInt(c));
		}
		

	}

}
