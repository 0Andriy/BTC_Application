<?php
function requests()
{
    $html = file_get_contents('https://btc-trade.com.ua/api/ticker/btc_uah');
    $decoded_json = json_decode($html, true);
    // echo($decoded_json["btc_uah"]["sell"]);
    return $decoded_json["btc_uah"]["sell"];
}
?>


<?php
function readDB()
{
    $file_array = file("DataBase-00.txt");
    
    return $file_array;
}
?>


<?php
function writeDB($arg_1)
{
    $fp = fopen("DataBase-00.txt", "a"); // Открываем файл в режиме записи
	$test = fwrite($fp, $arg_1); // Запись в файл
	if ($test) echo 'Данные в файл успешно занесены.';
	else echo 'Ошибка при записи в файл.';
	fclose($fp); //Закрытие файла
}
?>


<?php
function subscribe($mail)
{
    $arr = readDB();
    if (in_array($mail, $arr)) {
      echo 'Є такий користувач в базі';
    }else{
      echo 'Такого окристувача нема в базі';
      writeDB($mail);
    }
}
?>


<?php
function sendEmails()
{
    $arr = readDB();
    $cur = requests();
    
    $title = substr(htmlspecialchars(trim("Курсу BTC до UAH")), 0, 1000);
    $mess =  substr(htmlspecialchars(trim($cur)), 0, 1000000);
    // $from - от кого
    $from='test@test.com';
    
    foreach ($arr as &$to) {
        // $to - кому отправляем
        // функция, которая отправляет наше письмо.
        mail($to, $title, $mess, 'From:'.$from);
        echo 'Спасибо! Ваше письмо отправлено.';
    }
}
?>


<?php
echo("Виберіть операцію:\n1 -- Взнати курс BTC до UAH\n2 -- Підписатися на розсилку\n3 -- Зробити масово розсилку курсу");

switch ($i) {
    case 1:
        $cur = requests();
        echo($cur);
        break;
    case 2:
        $mail = "3@gmail.com";
        writeDB($mail);
        break;
    case 3:
        sendEmails();
        break;
}
?>