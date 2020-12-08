
## Build Image

* Option 1: `Run from dockerfile`
    ```
        ./rundocker.sh 
    ```
* Option 2: `Run from docker-compose`
    ```
        ./rundockerCompose.sh 
    ```

## Test API
* `Decode The PDF417 Image:` 
![Decode](doc/postManEx_decode.png)

* `Service Healthcheck:` 
![HealthCheck](doc/PostManHealthCheck.png)


## Zxing command line parser
* https://github.com/zxing/zxing/blob/b1c85db64e0ef13e7d8a4c9de32bd94c76eea5d8/javase/src/test/java/com/google/zxing/client/j2se/DecodeWorkerTestCase.java

* https://github.com/zxing/zxing/wiki/Getting-Started-Developing#javase
* `java -cp /home/cody/src/zxing-zxing-3.4.0/javase/target/javase-3.4.0-jar-with-dependencies.jar com.google.zxing.client.j2se.CommandLineRunner --multi --possible_formats DATA_MATRIX --try_harder data_matrix_and_QR.jpg
`
  
* `java -jar javase-3.4.1-SNAPSHOT-jar-with-dependencies.jar --help`
* `java -jar javase-3.4.1-SNAPSHOT-jar-with-dependencies.jar  --try_harder  test.jpg`
* `java -jar javase-3.4.1-SNAPSHOT-jar-with-dependencies.jar --possible_formats PDF_417 --try_harder  test.jpg`

