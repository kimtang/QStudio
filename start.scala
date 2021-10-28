
import scala.util.matching.Regex;
import java.awt.Font;
import java.util.TimeZone;
import javax.swing.UIManager;
import studio.kdb.Config;
import studio.kdb.Server;
import studio.ui.ExceptionGroup;
import studio.ui.StudioPanel;

TimeZone.setDefault(TimeZone.getTimeZone("GMT"));

if (System.getProperty("os.name", "").contains("OS X")) {
    System.setProperty("apple.laf.useScreenMenuBar", "true");
    System.setProperty("apple.awt.showGrowBox", "true");
    System
        .setProperty("com.apple.mrj.application.apple.menu.about.name", "Studio for kdb+");
    System.setProperty("com.apple.mrj.application.live-resize", "true");
    System.setProperty("com.apple.macos.smallTabs", "true");
    System.setProperty("com.apple.mrj.application.growbox.intrudes", "false");
}

if (Config.getInstance().getLookAndFeel() != null) {
    try {
        UIManager.setLookAndFeel(Config.getInstance().getLookAndFeel());
    } catch {
        // go on with default one        
        case ex: Exception => ex.printStackTrace()

    }
}

UIManager.put("Table.font", new javax.swing.plaf.FontUIResource("Monospaced", Font.PLAIN,UIManager.getFont("Table.font").getSize()));
System.setProperty("awt.useSystemAAFontSettings", "on");
System.setProperty("swing.aatext", "true");

var sub = StudioPanel.init(Array[String]())
var cfg = Config.getInstance()

def executeK4Query(l: String){
	println(l)
	sub.executeK4Query(l)}


def addSetServer(s: String) {
	println(s);
	var p = "/\\s(.+):(.+):(\\d*):(.*):(.*)".r;
	var r = p.findFirstMatchIn(s).get;
	var ss = new studio.kdb.Server();
	ss.setName(r.group(1));
	ss.setHost(r.group(2));
	ss.setPort(Integer.parseInt(r.group(3)));
	ss.setUsername(r.group(4));
	ss.setPassword(r.group(5));
	ss.setAuthenticationMechanism("Username and password");
    // var oldServer = cfg.getServer(r.group(1));
    // if(oldServer!=null){cfg.removeServer(oldServer);}
    // cfg.addServer(ss);
	sub.setServer(ss);
}