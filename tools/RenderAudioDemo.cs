// Build short licensed website examples using the unchanged application engine.
using System;using System.IO;using System.Text;using System.Globalization;using System.Diagnostics;using System.ComponentModel;
namespace PeakMp3Win7{
 internal static class RenderAudioDemo{
  static string Q(string s){return "\""+s+"\"";}
  [STAThread]static int Main(string[] args){try{
   string ff=args[0],input=args[1],output=args[2];Directory.CreateDirectory(output);
   ProcessingEngine engine=new ProcessingEngine(ff,new BackgroundWorker(),delegate(string k,string v){});
   ProcessResult analysis=engine.AnalyzeForPreview(input,false,true);
   for(int density=0;density<=10;density++){
    string dir=Path.Combine(output,"build-"+density);Directory.CreateDirectory(dir);
    JobOptions job=new JobOptions();job.Inputs=new string[]{input};job.OutputFolder=dir;job.DenseMode=true;job.DenseStrength=density;job.KnownAnalyses=new ProcessResult[]{analysis};engine.Convert(job);
    string from=Directory.GetFiles(dir,"*.mp3")[0],mp3=Path.Combine(output,"density-"+density+".mp3");File.Move(from,mp3);Directory.Delete(dir);
    Process p=new Process();p.StartInfo.FileName=ff;p.StartInfo.Arguments="-v error -nostdin -i "+Q(mp3)+" -ar 44100 -ac 2 -c:a pcm_f32le -f f32le -";p.StartInfo.UseShellExecute=false;p.StartInfo.CreateNoWindow=true;p.StartInfo.RedirectStandardOutput=true;p.Start();
    MemoryStream memory=new MemoryStream();byte[] buffer=new byte[16384];int read;while((read=p.StandardOutput.BaseStream.Read(buffer,0,buffer.Length))>0)memory.Write(buffer,0,read);p.WaitForExit();if(p.ExitCode!=0)throw new Exception("Decoded sample failed");
    byte[] bytes=memory.ToArray();float[] samples=new float[bytes.Length/4];Buffer.BlockCopy(bytes,0,samples,0,bytes.Length);int frames=samples.Length/2;
    StringBuilder json=new StringBuilder("{\"fps\":32,\"duration\":"+(frames/44100.0).ToString("0.000",CultureInfo.InvariantCulture)+",\"vu\":[");MeterEnvelope meter=new MeterEnvelope();
    for(int n=0;n*44100L/32<frames;n++){int offset=(int)(n*44100L/32);float l=0,r=0;ReferencePeakWindow.Measure(samples,offset,Math.Min(512,frames-offset),ref l,ref r);meter.Push(l,0,r,0,1.0/32);double db=Math.Max(-20,Math.Min(3,MeterEnvelope.Db(Math.Max(meter.Left,meter.Right))));if(n>0)json.Append(',');json.Append(db.ToString("0.000",CultureInfo.InvariantCulture));}
    json.Append("],\"wave\":[");for(int n=0;n<350;n++){float peak=0;for(int j=(int)(n*(long)frames/350);j<(n+1)*(long)frames/350;j++)peak=Math.Max(peak,Math.Max(Math.Abs(samples[j*2]),Math.Abs(samples[j*2+1])));if(n>0)json.Append(',');json.Append(peak.ToString("0.0000",CultureInfo.InvariantCulture));}json.Append("]}");File.WriteAllText(Path.Combine(output,"density-"+density+".json"),json.ToString(),new UTF8Encoding(false));
    Console.WriteLine(Path.GetFileName(output)+" density "+density+" exported and decoded");
   }return 0;
  }catch(Exception e){Console.Error.WriteLine(e);return 1;}}
 }
}
