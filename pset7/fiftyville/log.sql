-- Keep a log of any SQL queries you execute as you solve the mystery.


--  The theft took place on July 28, 2021 and that it took place on Humphrey Street.


SELECT description FROM crime_scene_reports
WHERE (year = 2021 AND month = 7 AND day = 28)
AND street = "Humphrey Street";
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.


SELECT transcript FROM interviews
WHERE (year = 2021 AND month = 7 AND day = 28);
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.


SELECT minute, license_plate FROM bakery_security_logs
WHERE (year = 2021 AND month = 7 AND day = 28)
AND (hour = 10 and minute < 25)
AND activity = "exit";
-- +--------+---------------+
-- | minute | license_plate |
-- +--------+---------------+
-- | 16     | 5P2BI95       |
-- | 18     | 94KL13X       |
-- | 18     | 6P58WS2       |
-- | 19     | 4328GD8       |
-- | 20     | G412CB7       |
-- | 21     | L93JTIZ       |
-- | 23     | 322W7JE       |
-- | 23     | 0NTHK55       |
-- +--------+---------------+


SELECT account_number, amount FROM atm_transactions
WHERE (year = 2021 AND month = 7 AND day = 28)
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";
-- +----------------+--------+
-- | account_number | amount |
-- +----------------+--------+
-- | 28500762       | 48     |
-- | 28296815       | 20     |
-- | 76054385       | 60     |
-- | 49610011       | 50     |
-- | 16153065       | 80     |
-- | 25506511       | 20     |
-- | 81061156       | 30     |
-- | 26013199       | 35     |
-- +----------------+--------+


SELECT caller, receiver FROM phone_calls
WHERE (year = 2021 AND month = 7 AND day = 28)
AND duration < 60;
-- +----------------+----------------+
-- |     caller     |    receiver    |
-- +----------------+----------------+
-- | (130) 555-0289 | (996) 555-8899 |
-- | (499) 555-9472 | (892) 555-8872 |
-- | (367) 555-5533 | (375) 555-8161 |
-- | (499) 555-9472 | (717) 555-1342 |
-- | (286) 555-6063 | (676) 555-6554 |
-- | (770) 555-1861 | (725) 555-3243 |
-- | (031) 555-6622 | (910) 555-3251 |
-- | (826) 555-1652 | (066) 555-9701 |
-- | (338) 555-6650 | (704) 555-2131 |
-- +----------------+----------------+


SELECT name, passport_number FROM people, bank_accounts
WHERE people.id = bank_accounts.person_id
AND license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE (year = 2021 AND month = 7 AND day = 28)
    AND (hour = 10 and minute < 25)
    AND activity = "exit"
)
AND account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE (year = 2021 AND month = 7 AND day = 28)
    AND atm_location = "Leggett Street"
    AND transaction_type = "withdraw"
)
AND phone_number IN (
    SELECT caller FROM phone_calls
    WHERE (year = 2021 AND month = 7 AND day = 28)
    AND duration < 60
);
-- +-------+-----------------+
-- | name  | passport_number |
-- +-------+-----------------+
-- | Bruce | 5773159633      |
-- | Diana | 3592750733      |
-- +-------+-----------------+


SELECT flights.id, hour, minute FROM flights, airports
WHERE airports.id = flights.origin_airport_id
AND (year = 2021 AND month = 7 AND day = 29)
AND city = "Fiftyville"
ORDER BY hour;
+----+------+--------+
| id | hour | minute |
+----+------+--------+
| 36 | 8    | 20     |
| 43 | 9    | 30     |
| 23 | 12   | 15     |
| 53 | 15   | 20     |
| 18 | 16   | 0      |
+----+------+--------+


SELECT passport_number FROM passengers
WHERE passport_number IN (
    SELECT passport_number FROM people, bank_accounts
    WHERE people.id = bank_accounts.person_id
    AND license_plate IN (
        SELECT license_plate FROM bakery_security_logs
        WHERE (year = 2021 AND month = 7 AND day = 28)
        AND (hour = 10 and minute < 25)
        AND activity = "exit"
    )
    AND account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE (year = 2021 AND month = 7 AND day = 28)
        AND atm_location = "Leggett Street"
        AND transaction_type = "withdraw"
    )
    AND phone_number IN (
        SELECT caller FROM phone_calls
        WHERE (year = 2021 AND month = 7 AND day = 28)
        AND duration < 60
    )
)
AND flight_id = (
    SELECT flights.id FROM flights, airports
    WHERE airports.id = flights.origin_airport_id
    AND (year = 2021 AND month = 7 AND day = 29)
    AND city = "Fiftyville"
    ORDER BY hour
    LIMIT 1
);
-- +-----------------+
-- | passport_number |
-- +-----------------+
-- | 5773159633      |
-- +-----------------+


SELECT * FROM people
WHERE passport_number = (
    SELECT passport_number FROM passengers
    WHERE passport_number IN (
        SELECT passport_number FROM people, bank_accounts
        WHERE people.id = bank_accounts.person_id
        AND license_plate IN (
            SELECT license_plate FROM bakery_security_logs
            WHERE (year = 2021 AND month = 7 AND day = 28)
            AND (hour = 10 and minute < 25)
            AND activity = "exit"
        )
        AND account_number IN (
            SELECT account_number FROM atm_transactions
            WHERE (year = 2021 AND month = 7 AND day = 28)
            AND atm_location = "Leggett Street"
            AND transaction_type = "withdraw"
        )
        AND phone_number IN (
            SELECT caller FROM phone_calls
            WHERE (year = 2021 AND month = 7 AND day = 28)
            AND duration < 60
        )
    )
    AND flight_id = (
        SELECT flights.id FROM flights, airports
        WHERE airports.id = flights.origin_airport_id
        AND (year = 2021 AND month = 7 AND day = 29)
        AND city = "Fiftyville"
        ORDER BY hour
        LIMIT 1
    )
);
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+


SELECT city FROM flights, airports
WHERE airports.id = destination_airport_id
AND flights.id = (
    SELECT flights.id FROM flights, airports
    WHERE airports.id = flights.origin_airport_id
    AND (year = 2021 AND month = 7 AND day = 29)
    AND city = "Fiftyville"
    ORDER BY hour
    LIMIT 1
);
-- +---------------+
-- |     city      |
-- +---------------+
-- | New York City |
-- +---------------+


SELECT receiver FROM phone_calls
WHERE (year = 2021 AND month = 7 AND day = 28)
AND duration < 60
AND caller = (
    SELECT phone_number FROM people
    WHERE passport_number = (
        SELECT passport_number FROM passengers
        WHERE passport_number IN (
            SELECT passport_number FROM people, bank_accounts
            WHERE people.id = bank_accounts.person_id
            AND license_plate IN (
                SELECT license_plate FROM bakery_security_logs
                WHERE (year = 2021 AND month = 7 AND day = 28)
                AND (hour = 10 and minute < 25)
                AND activity = "exit"
            )
            AND account_number IN (
                SELECT account_number FROM atm_transactions
                WHERE (year = 2021 AND month = 7 AND day = 28)
                AND atm_location = "Leggett Street"
                AND transaction_type = "withdraw"
            )
            AND phone_number IN (
                SELECT caller FROM phone_calls
                WHERE (year = 2021 AND month = 7 AND day = 28)
                AND duration < 60
            )
        )
        AND flight_id = (
            SELECT flights.id FROM flights, airports
            WHERE airports.id = flights.origin_airport_id
            AND (year = 2021 AND month = 7 AND day = 29)
            AND city = "Fiftyville"
            ORDER BY hour
            LIMIT 1
        )
    )
);
-- +----------------+
-- |    receiver    |
-- +----------------+
-- | (375) 555-8161 |
-- +----------------+


SELECT * FROM people
WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE (year = 2021 AND month = 7 AND day = 28)
    AND duration < 60
    AND caller = (
        SELECT phone_number FROM people
        WHERE passport_number = (
            SELECT passport_number FROM passengers
            WHERE passport_number IN (
                SELECT passport_number FROM people, bank_accounts
                WHERE people.id = bank_accounts.person_id
                AND license_plate IN (
                    SELECT license_plate FROM bakery_security_logs
                    WHERE (year = 2021 AND month = 7 AND day = 28)
                    AND (hour = 10 and minute < 25)
                    AND activity = "exit"
                )
                AND account_number IN (
                    SELECT account_number FROM atm_transactions
                    WHERE (year = 2021 AND month = 7 AND day = 28)
                    AND atm_location = "Leggett Street"
                    AND transaction_type = "withdraw"
                )
                AND phone_number IN (
                    SELECT caller FROM phone_calls
                    WHERE (year = 2021 AND month = 7 AND day = 28)
                    AND duration < 60
                )
            )
            AND flight_id = (
                SELECT flights.id FROM flights, airports
                WHERE airports.id = flights.origin_airport_id
                AND (year = 2021 AND month = 7 AND day = 29)
                AND city = "Fiftyville"
                ORDER BY hour
                LIMIT 1
            )
        )
    )
);
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
-- +--------+-------+----------------+-----------------+---------------+
