<?php

function gen_pwd($seed) {
    mt_srand($seed);
    $token_length = 12;
    // from https://devco.re/blog/2019/06/21/operation-crack-hacking-IDA-Pro-installer-PRNG-from-an-unusual-way-en/
    $search_space = 'abcdefghijkmpqrstuvwxyzABCDEFGHJKLMPQRSTUVWXYZ23456789';
    $search_space_length = strlen($search_space);
    $token = '';
    for ($i = 0; $i < $token_length; $i++) {
        $index = mt_rand(0, $search_space_length - 1);
        $character = $search_space[$index];
        $token = $token . $character;
    }
    return $token;
}

for ($i = 0; $i < 4294967296; $i++) {
    print(gen_pwd($i) . "\n");
}

?>
