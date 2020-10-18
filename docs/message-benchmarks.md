# Message benchmarks

| serializer          | bench_description   |   duration_seconds |   repetitions | payload_byte_size   | message_overhead   | message_size   | object_size   | total_overhead   |
|---------------------|---------------------|--------------------|---------------|---------------------|--------------------|----------------|---------------|------------------|
| JsonSerializer      | Small payload       |              2.527 |        100000 | 1.6 kB              | 288 Bytes          | 5.4 kB         | 5.1 kB        | 28.8 MB          |
| JsonSerializer      | Large payload       |              4.381 |          1000 | 399.3 kB            | 48.2 kB            | 1.1 MB         | 1.0 MB        | 48.2 MB          |
| JsonSerializer      | Massive payload     |              5.533 |            10 | 40.1 MB             | 4.8 MB             | 105.2 MB       | 100.4 MB      | 48.0 MB          |
| JsonSerializer      | Nested              |              0.872 |            10 | 11.5 MB             | 4.7 kB             | 22.4 MB        | 22.4 MB       | 46.6 kB          |
| UJsonSerializer     | Small payload       |              2.071 |        100000 | 1.6 kB              | 288 Bytes          | 6.1 kB         | 5.8 kB        | 28.8 MB          |
| UJsonSerializer     | Large payload       |              3.692 |          1000 | 399.3 kB            | 48.2 kB            | 1.7 MB         | 1.7 MB        | 48.2 MB          |
| UJsonSerializer     | Massive payload     |              5.983 |            10 | 40.1 MB             | 4.8 MB             | 171.4 MB       | 166.6 MB      | 48.0 MB          |
| UJsonSerializer     | Nested              |              0.926 |            10 | 11.5 MB             | 4.7 kB             | 37.2 MB        | 37.2 MB       | 46.6 kB          |
| RapidJsonSerializer | Small payload       |              2.31  |        100000 | 1.6 kB              | 288 Bytes          | 6.1 kB         | 5.8 kB        | 28.8 MB          |
| RapidJsonSerializer | Large payload       |              4.404 |          1000 | 399.3 kB            | 48.2 kB            | 1.7 MB         | 1.7 MB        | 48.2 MB          |
| RapidJsonSerializer | Massive payload     |              7.534 |            10 | 40.1 MB             | 4.8 MB             | 171.4 MB       | 166.6 MB      | 48.0 MB          |
| RapidJsonSerializer | Nested              |              1.08  |            10 | 11.5 MB             | 4.7 kB             | 37.2 MB        | 37.2 MB       | 46.6 kB          |
| OrJsonSerializer    | Small payload       |              2.19  |        100000 | 1.6 kB              | 304 Bytes          | 5.4 kB         | 5.1 kB        | 30.4 MB          |
| OrJsonSerializer    | Large payload       |              3.829 |          1000 | 399.3 kB            | 49.2 kB            | 1.1 MB         | 1.0 MB        | 49.2 MB          |
| OrJsonSerializer    | Massive payload     |              5.394 |            10 | 40.1 MB             | 4.8 MB             | 105.2 MB       | 100.4 MB      | 48.2 MB          |
| OrJsonSerializer    | Nested              |              0.834 |            10 | 11.5 MB             | 4.8 kB             | 22.4 MB        | 22.4 MB       | 47.6 kB          |