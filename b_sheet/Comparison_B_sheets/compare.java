import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class BListProcessor {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			// Fetching data from CSR database and write them to a new file.
			/*
			 * InputStreamReader csrFile = new InputStreamReader(new
			 * FileInputStream("D:\\CSR\\pdf\\csr_index.csv"), StandardCharsets.UTF_8);
			 * BufferedReader csrReader = new BufferedReader(csrFile); BufferedWriter
			 * csrWriter = new BufferedWriter(new FileWriter("D:\\CSR\\pdf\\output.csv"));
			 * String line = null; int count = 0;
			 *
			 * while ((line = csrReader.readLine()) != null) { String item[] =
			 * line.split(","); csrWriter.write(item[8]); for (int i = 214; i < 369; i++) {
			 * csrWriter.write("," + item[i]); } csrWriter.newLine();
			 * 
			 * System.out.println(item.length); System.out.print(item[8].trim()); for (int i
			 * = 218; i < 369; i++) { System.out.print(" " + item[i].trim()); }
			 * System.out.println();
			 * 
			 * count++; } csrWriter.close(); csrReader.close();
			 */

			// Processing auto-recognition data and database data
			InputStreamReader outputFile = new InputStreamReader(new FileInputStream("output.csv"),
					StandardCharsets.UTF_8);
			BufferedReader outputFileReader = new BufferedReader(outputFile);
			InputStreamReader BListFile = new InputStreamReader(
					new FileInputStream("gri_pointers_b.csv"), StandardCharsets.UTF_8);
			BufferedReader BListFileReader = new BufferedReader(BListFile);

			String outputList[][] = new String[602][]; // 602 lines to be processed

			// Just trying Lambda
			/*
			 * Arrays.stream(outputList).forEach(array -> { String line = null; try { if
			 * ((line = outputFileReader.readLine()) != null) { array = line.split(","); } }
			 * catch (IOException e) { // TODO Auto-generated catch block
			 * e.printStackTrace(); } finally { // Arrays.stream(array).forEach(item ->
			 * System.out.println(item)); array[0].replace("臺", "台");
			 * array[0].replace("(又又)", "雙"); } });
			 */

			String line = null;
			for (int i = 0; i < outputList.length; i++) {
				if ((line = outputFileReader.readLine()) != null) {
					line.replace("臺", "台"); // handle common changeable words
					line.replace("(又又)", "雙"); // handle unique words
					outputList[i] = line.split(",");
				}
			}

			String BList[][] = new String[512][]; // 512 lines to be processed

			// Just trying Lambda
			/*
			 * Arrays.stream(BList).forEach(array -> { String line = null; try { if ((line =
			 * BListFileReader.readLine()) != null) { array = line.split(","); } } catch
			 * (Exception e) { // TODO: handle exception } finally { //
			 * Arrays.stream(array).forEach(item -> System.out.println(item));
			 * array[0].replace("臺", "台"); String corpName[] = array[0].split("_"); array[0]
			 * = corpName[1]; } });
			 */

			for (int i = 0; i < BList.length; i++) {
				if ((line = BListFileReader.readLine()) != null) {
					line.replace("臺", "台"); // handle common changeable words
					BList[i] = line.split(",");
					BList[i][1] = BList[i][1].split("_")[1];
				}
			}

			outputFileReader.close();
			BListFileReader.close();

			// Arrays.stream(BList).forEach(array -> Arrays.stream(array).forEach(item ->
			// System.out.println(item + " ")));

			BufferedWriter writer = new BufferedWriter(new FileWriter("compare_result.csv"));

			// Title
			for (int i = 0; i < outputList[0].length; i++) {
				// System.out.println(outputList[i][0]);
				writer.write(outputList[0][i].trim() + ",");
			}
			writer.newLine();

			// Differentiate the differences between two data
			for (int i = 1; i < BList.length; i++) {
				boolean trigger = false;
				for (int j = 1; j < outputList.length; j++) {
					for (int l = 0; l < BList[i][1].length(); l++) {
						if (outputList[j][0].contains("" + BList[i][1].charAt(l))) {
							trigger = true;
						} else {
							trigger = false;
							break;
						}
					}
					if (trigger) {
						writer.write(outputList[j][0]);
						boolean Unprocessable = false;
						for (int k = 1; k < 137; k++) {
							if (BList[i][k + 1].equals("0")) {
								Unprocessable = true;
							} else {
								Unprocessable = false;
								break;
							}
						}

						for (int k = 1; k < 137; k++) {
							if (Unprocessable) {
								writer.write(",-1"); //Unprocessable
							} else {
								if (outputList[j][k].equals(BList[i][k + 1])) {
									writer.write(",1"); // identical
								} else if (BList[i][k + 1].isBlank() || BList[i][k + 1].isEmpty()
										|| BList[i][k + 1] == null) {
									writer.write(", N/A"); //no data
								} else {
									writer.write(",0"); // Not identical
								}
							}
						}
						writer.newLine();
						break;
					}
				}
			}
			writer.close();

		} catch (FileNotFoundException e) {
			// TODO: handle exception
			e.printStackTrace();
		} catch (IOException e) {
			// TODO: handle exception
			e.printStackTrace();
		} catch (NullPointerException e) {
			// TODO: handle exception
			e.printStackTrace();
		} catch (ArrayIndexOutOfBoundsException e) {
			// TODO: handle exception
			e.printStackTrace();
		} catch (StringIndexOutOfBoundsException e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}
}