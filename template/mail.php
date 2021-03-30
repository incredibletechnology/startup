<?php
	if(isset($_POST['submit'])) {
		
    $email=$_POST['email'];
    $name=$_POST['name'];
    $subject=$_POST['subject'];
    $message=$_POST['message'];
    $number=$_POST['number'];
	
	echo $email." ".$name." ".$subject." ".$message;
	
	$myemail = "";   #Your business mail account
	$password = "";				#Mail accounnt password

	
   require_once "PHPMailer/PHPMailerAutoload.php";
   $mail = new PHPMailer();
   $mail ->IsSmtp();
   $mail ->SMTPDebug = 2;
   $mail ->SMTPAuth = true;
   $mail ->SMTPSecure = 'ssl';
   $mail ->Host = "smtp.gmail.com";
   $mail ->Port = 465; // or 587
   $mail ->IsHTML(TRUE);
   $mail ->Username = $myemail;
   $mail ->From = $email;
   $mail ->FromName = $email;
   $mail ->Password = $password;
   #$mail ->SetFrom($myemail);
   $mail ->Subject = $email; # Sender's Email
   $mail ->Body = '<h1 align="center">'.$subject.'</h1><br/>
					<ul>
						<li>Name: '.$name.'</li>
						<li>Contact No.: '.$number.'</li>
						<li>Email Id: '.$email.'</li>
						<li>Subject: '.$subject.'</li>
						<li>Message: '.$message.'</li>
					</ul>';
   $mail ->AddAddress($myemail); // Send mail To
   #$mail->AddCC($email);

   if(!$mail->Send())
   {
       #echo "Mail Not Sent".$mail->ErrorInfo;
	   header("location: contact.php?sent=false");
   }
   else
   {
       header("location: contact.php?sent=true");
	   #echo "Mail Sent";
   } 
   
}
?>