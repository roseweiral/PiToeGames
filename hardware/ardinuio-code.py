void setup() {
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readString();
        Serial.print("You sent: ");
        Serial.println(data);
    }
    delay(100);
}
