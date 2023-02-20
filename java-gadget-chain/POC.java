// Basic Java serialisation/deserialisation (General POC version)
// To inject other data, rewrite the object with the desired data and read it through the Deserialize() function.

// File Input/Output bytes
import java.io.FileInputStream;
import java.io.FileOutputStream;
// Serialisation/Deserialisation of Input's Object.
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
// Mark object to be deserialised.
import java.io.Serializable;


public class POC implements Serializable {
	private String data;

	public POC(String testData) {
		this.data = testData;
	}

	public String getData() {
		return data;
	}


  public static void Serialize() {
    try {
        // Object Creation
        POC poctest = new POC("This is a POC!");
        // Creating output stream and writing the serialized object
        FileOutputStream outfile = new FileOutputStream("serialized.object");
        ObjectOutputStream outstream = new ObjectOutputStream(outfile);
        outstream.writeObject(poctest);
        // Closing the stream
        outstream.close();
        System.out.println("Serialized object saved to serialized.object");
    } catch (Exception e) {
        System.out.println(e);
    }}

  public static void Deserialize() {
    try{
        ObjectInputStream in = new ObjectInputStream(new FileInputStream("serialized.object"));
        POC poctest = (POC)in.readObject();
        // Printing the data of the serialized object
        System.out.println("Object's data: " + poctest.data);
        // Closing the stream
        in.close();
    } catch (Exception e) {
            System.out.println(e);
            }
    }

  public static void main(String args[]) {
        POC.Serialize();
        POC.Deserialize();
    }

}
