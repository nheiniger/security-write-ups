08 - Snd Mny
------------
In this challenge we need to exploit an activity of the Android application. After decompiling the APK file we can read the details of the activity in the AndroidManifest.xml:
```xml
<activity android:label="@string/title_activity_snd" android:name="ps.hacking.hackyeaster.android.SndActivity">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/*" />
    </intent-filter>
</activity>
```

We see the activity name and the intent filters. When looking at the code we see the following method:
```java
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    requestWindowFeature(1);
    getWindow().setFlags(1024, 1024);
    setContentView(R.layout.activity_snd);
    Intent intent = getIntent();
    String action = intent.getAction();
    String type = intent.getType();
    if ("android.intent.action.SEND".equals(action) && type != null && HTTP.PLAIN_TEXT_TYPE.equals(type)) {
        String text = intent.getStringExtra("android.intent.extra.TEXT");
        if (text != null && "c95259de1fd719814daef8f1dc4bd64f9d885ff0".equals(sha1(text.toLowerCase()))) {
            ((TextView) findViewById(R.id.sndTextView)).setText("Thank you!!");
            ImageView image = (ImageView) findViewById(R.id.sndImageView);
            byte[] decodedString = Base64.decode(new StringBuilder(getString(R.string.e) + "ROBVi").reverse().toString(), 0);
            image.setImageBitmap(BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length));
        }
    }
}
```

So we need to send our action with mime type `text/plain` and with an extra string that when hashed using SHA1 will give the hash `c95259de1fd719814daef8f1dc4bd64f9d885ff0`. Given the name of the activity we guess that the value might be money and this can be checked via:
```bash
$ echo -n 'money' | sha1sum
c95259de1fd719814daef8f1dc4bd64f9d885ff0  -
```

Then we can use drozer (one useful example is given in [1]) to start the activity with the following command that includes all the parameters retrieved previously:
```
dz> run app.activity.start --component ps.hacking.hackyeaster.android ps.hacking.hackyeaster.android.SndActivity --action android.intent.action.SEND --category android.intent.category.BROWSABLE --mimetype text/plain --extra string android.intent.extra.TEXT "money"
```

This will display the egg in the application on the phone:
![](./08/egg08.png)

\[1\]: Mobile penetration testing on Android using Drozer, <https://securitycafe.ro/2015/07/08/mobile-penetration-testing-using-drozer/>
