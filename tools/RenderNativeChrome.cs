// Export real application control pixels for the website, without a second UI design.
using System;using System.IO;using System.Text;using System.Reflection;using System.Collections.Generic;using System.Drawing;using System.Drawing.Imaging;using System.Windows.Forms;
namespace PeakMp3Win7{
 internal static class RenderNativeChrome{
  static string assets,output;static int language;
  static readonly string[] langs={"ru","de","en"};
  static readonly string[] ids={"techno","electronic","pop"};
  static readonly string[] titles={"EDM Detection Mode","Electro (Sketch)","Life of Riley"};
  static VintageState State(){VintageState s=new VintageState();s.Language=language;s.HasFile=true;s.Density=7;s.Volume=60;s.Vu=-20;s.Duration=24;s.QueueCount=3;s.Transport=3;s.Processed=true;s.FileName=titles[0];s.Metadata="Kevin MacLeod · MP3 · 44.1 kHz · 320 kb/s";s.Label=new RecordName("Kevin MacLeod",titles[0]);return s;}
  static Bitmap Render(VintageState s,string hover){using(VintageSurface v=new VintageSurface(assets)){
   v.Size=new Size(973,1616);v.CreateControl();if(hover!="")typeof(VintageSurface).GetField("hover",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(v,hover);v.Bind(s);Bitmap b=new Bitmap(973,1616,PixelFormat.Format32bppPArgb);v.DrawToBitmap(b,new Rectangle(0,0,973,1616));return b;
  }}
  static void Atlas(string name,Rectangle box,int count,int columns,Action<VintageState,int> change,string[] hover){
   Bitmap sheet=new Bitmap(box.Width*columns,box.Height*((count+columns-1)/columns),PixelFormat.Format32bppPArgb);
   using(Graphics g=Graphics.FromImage(sheet)){g.Clear(Color.Transparent);for(int i=0;i<count;i++){VintageState s=State();change(s,i);using(Bitmap b=Render(s,hover==null?"":hover[i]))g.DrawImage(b,new Rectangle((i%columns)*box.Width,(i/columns)*box.Height,box.Width,box.Height),box,GraphicsUnit.Pixel);}}
   sheet.Save(Path.Combine(output,name+".png"),ImageFormat.Png);sheet.Dispose();Console.WriteLine(name);
  }
  static void ClearValues(Control parent){foreach(Control child in parent.Controls){if(child is TextBox)child.Text="";if(child is Label&&child.Text=="0 dBFS")child.Text="";ClearValues(child);}}
  static void Capture(Form dialog,string name,int w,int h){dialog.StartPosition=FormStartPosition.Manual;dialog.Location=new Point(-20000,-20000);dialog.ShowInTaskbar=false;ClearValues(dialog);dialog.Show();Application.DoEvents();using(Bitmap b=new Bitmap(w,h)){dialog.DrawToBitmap(b,new Rectangle(0,0,w,h));b.Save(Path.Combine(output,name+".png"),ImageFormat.Png);}dialog.Close();}
  static string Q(string s){return "\""+s.Replace("\\","\\\\").Replace("\"","\\\"").Replace("\r","\\r").Replace("\n","\\n")+"\"";}
  [STAThread]static int Main(string[] args){try{
   assets=args[0];output=args[1];Directory.CreateDirectory(output);Application.EnableVisualStyles();Application.SetCompatibleTextRenderingDefault(false);
   if(args.Length>2&&args[2]=="dialogs"){for(int sound=0;sound<3;sound++)File.WriteAllBytes(Path.Combine(output,"sound-"+sound+".wav"),UiSounds.Wave(sound));for(language=0;language<3;language++){
    using(StudioCalibrationDialog dialog=new StudioCalibrationDialog(language,0))Capture(dialog,"calibration-"+langs[language],400,246);
    using(DensityInput dialog=new DensityInput(7,language))Capture(dialog,"density-"+langs[language],440,245);
   }return 0;}
   language=0;Atlas("knob",new Rectangle(342,524,278,278),11,11,delegate(VintageState s,int i){s.Density=i;},null);
   Atlas("transport",new Rectangle(52,1088,124,214),3,3,delegate(VintageState s,int i){s.Requested=i==1;s.Playing=i==1;s.Transport=i==0?3:i;s.Paused=i==2;},null);
   Atlas("comparison",new Rectangle(48,1404,204,90),2,2,delegate(VintageState s,int i){s.Processed=i==1;},null);
   Atlas("volume",new Rectangle(835,1276,100,210),101,10,delegate(VintageState s,int i){s.Volume=i;},null);
   Atlas("speaker",new Rectangle(860,1490,70,55),4,4,delegate(VintageState s,int i){s.Volume=new int[]{0,25,55,95}[i];},null);
   using(Bitmap paper=(Bitmap)Image.FromFile(Path.Combine(assets,"label-paper.png")))for(int i=0;i<3;i++)using(Bitmap label=RecordLabel.Create(paper,new RecordName("Kevin MacLeod",titles[i])))label.Save(Path.Combine(output,"label-"+ids[i]+".png"),ImageFormat.Png);
   for(language=0;language<3;language++){
    string lang=langs[language];using(Bitmap b=Render(State(),""))b.Save(Path.Combine(output,"base-"+lang+".png"),ImageFormat.Png);
    Rectangle[] boxes={new Rectangle(50,529,194,102),new Rectangle(50,667,194,102),new Rectangle(726,529,194,102),new Rectangle(726,667,194,102)};
    int[] values={2,5,8,10};using(Bitmap atlas=new Bitmap(194*8,102,PixelFormat.Format32bppPArgb)){
     using(Graphics g=Graphics.FromImage(atlas))for(int n=0;n<4;n++)for(int on=0;on<2;on++){VintageState s=State();s.Density=on==1?values[n]:7;using(Bitmap b=Render(s,""))g.DrawImage(b,new Rectangle((n*2+on)*194,0,194,102),boxes[n],GraphicsUnit.Pixel);}
     atlas.Save(Path.Combine(output,"presets-"+lang+".png"),ImageFormat.Png);
    }
    Atlas("caption-"+lang,new Rectangle(280,799,403,42),11,11,delegate(VintageState s,int i){s.Density=i;},null);
    Atlas("file-"+lang,new Rectangle(174,859,728,88),3,3,delegate(VintageState s,int i){s.FileName=titles[i];},null);
    Atlas("queue-"+lang,new Rectangle(638,1509,218,44),3,3,delegate(VintageState s,int i){s.QueueIndex=i;},null);
    Atlas("export-"+lang,new Rectangle(337,1490,300,75),2,2,delegate(VintageState s,int i){},new string[]{"","export"});
    using(StudioCalibrationDialog dialog=new StudioCalibrationDialog(language,0))Capture(dialog,"calibration-"+lang,400,246);
    using(DensityInput dialog=new DensityInput(7,language))Capture(dialog,"density-"+lang,440,245);
    StringBuilder json=new StringBuilder("{");bool first=true;Dictionary<string,string[]> words=(Dictionary<string,string[]>)typeof(L10n).GetField("Words",BindingFlags.NonPublic|BindingFlags.Static).GetValue(null);
    foreach(KeyValuePair<string,string[]> item in words){if(!first)json.Append(',');first=false;json.Append(Q(item.Key)+":"+Q(item.Value[language]));}json.Append('}');File.WriteAllText(Path.Combine(output,"locale-"+lang+".json"),json.ToString(),new UTF8Encoding(false));
   }
   Console.WriteLine("Native chrome exported from VintageSurface, RU/DE/EN");return 0;
  }catch(Exception e){Console.Error.WriteLine(e);return 1;}}
 }
}
