using System.Text;

namespace DataCompression
{
    public class Logger
    {
        public string Title { get; set; }
        public string Message { get; set; }
        public string log_path => "./log.txt";

        public Logger(string title, string message)
        {
            Title = title;
            Message = message;
        }

        public Logger()
        {
            Title = "No Title Set";
            Message = "No Message Set";
        }

        public void Log(string title, string message)
        {
            this.Title = title.ToUpper();
            this.Message = message;

            // Ensure File Exists
            if (!File.Exists(log_path))
            {
                // Using block to ensure the file and writer is closed after creation
                using (FileStream fs = File.Create(log_path))
                {
                    using (StreamWriter writer = new StreamWriter(fs))
                    {
                        writer.Write("\n[DATA COMPRESSION ERROR LOG]\n          [s2k]\n\n____________________________\n");
                    }
                }
            }

            // Console Logging
            Console.WriteLine(this.ToString());

            // Error File Logging
            string log_entry = CreateLogEntry();
            AppendToLogFile(log_entry);

        }

        private void AppendToLogFile(string log_entry)
        {
            using (StreamWriter writer = new StreamWriter(log_path, true))
            {
                writer.WriteLineAsync(log_entry);
            }
        }

        private string CreateLogEntry()
        {

            return $"   <Time: {DateTime.Now}> : [{this.Title}]: {this.Message}";
        }

        public override string ToString()
        {
            return $"[{this.Title}]: {this.Message}";
        }
    }
}