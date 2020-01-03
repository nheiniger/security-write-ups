24 - Your Passport, please
--------------------------
I'm not really sure what was more challenging here, installing Eclipse and make it work with Maven, dependencies and all the classpath issues or the challenge itself... In the end, for me the challenge is summarized as pick some code on existing open source projects on GitHub, paste it in the main Java method, correct the errors and ... done already.

I hereby gratefully thank projects [1] and [2] for their code, I borrowed a bit of each to get mine working. The final `JMRTDMain.java` file is as follows:
```java
package ch.he17.epassclient;

import java.io.DataInputStream;
import java.io.IOException;

import java.util.ArrayList;
import java.util.List;

import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;

import org.apache.commons.codec.binary.Base64;
import org.jmrtd.BACKeySpec;
import org.jmrtd.PassportService;
import org.jmrtd.lds.icao.DG2File;
import org.jmrtd.lds.icao.LDS;
import org.jmrtd.lds.iso19794.FaceImageInfo;
import org.jmrtd.lds.iso19794.FaceInfo;

import ch.he17.epassclient.terminal.HE17Terminal;
import net.sf.scuba.smartcards.CardFileInputStream;
import net.sf.scuba.smartcards.CardService;
import net.sf.scuba.smartcards.CardServiceException;

public class JMRTDMain {

    public static void main(String[] args) throws CardServiceException, CardException, IOException {
        CardTerminal cardTerminal = new HE17Terminal();
        CardService cService = CardService.getInstance(cardTerminal);
        PassportService passService = new PassportService(cService);
        cardTerminal.waitForCardPresent(1000);

        passService.open();
        passService.sendSelectApplet(false);

        // "Authentication" using BAC
        BACKeySpec bacKey = new BACKeySpec() {

            public String getDocumentNumber() {
                return "P01234567";
            }

            public String getDateOfBirth() {
                return "770707";
            }

            public String getDateOfExpiry() {
                return "210101";
            }
        };

        passService.doBAC(bacKey);
        
        // Now get the DG2 File for the picture
        LDS lds = new LDS();
        DG2File dg2File;
        CardFileInputStream dg2In = passService.getInputStream(PassportService.EF_DG2);
        lds.add(PassportService.EF_DG2, dg2In, dg2In.getLength());
        dg2File = lds.getDG2File();
        
        List<FaceImageInfo> allFaceImageInfos = new ArrayList<>();
        List<FaceInfo> faceInfos = dg2File.getFaceInfos();
        for (FaceInfo faceInfo : faceInfos) {
            allFaceImageInfos.addAll(faceInfo.getFaceImageInfos());
        }

        if (!allFaceImageInfos.isEmpty()) {
            FaceImageInfo faceImageInfo = allFaceImageInfos.iterator().next();

            int imageLength = faceImageInfo.getImageLength();
            DataInputStream dataInputStream = new DataInputStream(faceImageInfo.getImageInputStream());
            byte[] buffer = new byte[imageLength];
            dataInputStream.readFully(buffer, 0, imageLength);

            // Output a base64 encoded string to the console
            System.out.println(Base64.encodeBase64String(buffer));
        }
        
        passService.close();
    }
}

```

A small modification must also be done in `HE17Terminal.java`, line 21 must be changed to:
```java
            return new HE17Card(new Socket("hackyeaster.hacking-lab.com", 7777));
```

When running this code in Eclipse, lots of debug info is displayed and at the end our Base64 encoded string. The final step is to decode the Base64 to get the actual picture using:
```bash
$ echo -n 'BASE64DATA' | base64 -d > egg24.png
```

And I got the last egg:  
![](./24/egg24.jpg)

\[1\]: A sample android app that reads e-passports, <https://github.com/Glamdring/epassport-reader>
\[2\]: e-Passport NFC Reader Android app, <https://github.com/tananaev/passport-reader>
