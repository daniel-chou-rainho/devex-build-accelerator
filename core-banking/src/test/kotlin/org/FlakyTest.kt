package org.example.utilities

import org.junit.jupiter.api.Test
import java.util.Random

class FlakyTest {

    @Test
    fun `verify payment gateway connection`() {
        // Simulate a network call that fails 30% of the time
        val networkInstability = Random().nextInt(10)
        
        if (networkInstability < 3) {
            throw RuntimeException("503 Service Unavailable: Payment Gateway timed out")
        }
        
        println("Payment Gateway Connected Successfully")
    }
}