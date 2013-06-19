
import scala.util.matching.Regex

def startStudio() : studio.ui.Studio = {
	return sublime.SublimeVersion.init(Array[String]());
}

var sub = startStudio()

def executeK4Query(l: String){
	println(l)
	sub.executeK4Query(l)}

def chart(){sub.chart()}

def addSetServer(s: String) {
	println(s)
	var p = "/\\s(.+):(.+):(\\d{1,4}):(.*):(.*)".r;
	var r = p.findFirstMatchIn(s).get;
	var ss = new studio.kdb.Server();
	ss.setName(r.group(1));
	ss.setHost(r.group(2));
	ss.setPort(Integer.parseInt(r.group(3)));
	ss.setUsername(r.group(4));
	ss.setPassword(r.group(5));
	ss.setAuthenticationMechanism("Username and password");
	sub.addServer(ss);
	sub.setServer(ss);
}