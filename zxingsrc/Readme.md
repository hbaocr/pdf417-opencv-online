# Read more information here

* https://github.com/zxing/zxing/issues/518
* https://github.com/zxing/zxing/wiki/Getting-Started-Developing#javase
* https://github.com/zxing/zxing/issues/518
  
* https://github.com/zxing/zxing/blob/b1c85db64e0ef13e7d8a4c9de32bd94c76eea5d8/javase/src/test/java/com/google/zxing/client/j2se/DecodeWorkerTestCase.java

## Build zxing for java

* Install `maven tool`
  
```
brew install maven
```
* Build Zxing for java : `javase-3.4.2-SNAPSHOT-jar-with-dependencies.jar` will be found in `zxing/javase/target/` after maven build
```
git clone git@github.com:zxing/zxing.git
cd zxing
mvn install -DskipTests
cd javase
mvn -DskipTests package assembly:single
```
  
* `java -jar javase-3.4.1-SNAPSHOT-jar-with-dependencies.jar --help`
* `java -jar javase-3.4.1-SNAPSHOT-jar-with-dependencies.jar  --try_harder  test.jpg`
* `java -jar javase-3.4.1-SNAPSHOT-jar-with-dependencies.jar --possible_formats PDF_417 --try_harder  test.jpg`

* `java -jar javase-3.4.2-SNAPSHOT-jar-with-dependencies.jar --possible_formats PDF_417 --try_harder  test.jpg`

java -cp javase-3.4.2-20201107.150950-1.jar com.google.zxing.client.j2se.CommandLineRunner --possible_formats PDF_417 --try_harder  test.jpg