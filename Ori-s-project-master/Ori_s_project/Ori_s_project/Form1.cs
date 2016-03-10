using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Threading;
using System.Net.Sockets;
using System.Diagnostics;

namespace Ori_s_project
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            

        }

        private void StartPythonEngine()
        {
            try
            {
                // Start python engine
                pythonEngineProcess = new Process();
                pythonEngineProcess.StartInfo.FileName = @"C:\Python27\python.exe";
                pythonEngineProcess.StartInfo.Arguments = PythonEngine;
                pythonEngineProcess.StartInfo.WorkingDirectory = AppDomain.CurrentDomain.BaseDirectory;
                //####
                pythonEngineProcess.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
                pythonEngineProcess.Start();
            }
            catch (Win32Exception e)
            {
                EndProcess(e);
            }
            catch (ObjectDisposedException e)
            {
                EndProcess(e);
            }
            catch (InvalidOperationException e)
            {
                EndProcess(e);
            }
            catch (Exception e)
            {
                EndProcess(e);
            }
        }

        private void EndProcess(Exception e)
        {
            PrintToLog(e.Message, Color.Red);
            if (pythonEngineProcess != null)
            {
                pythonEngineProcess.Dispose();
                pythonEngineProcess = null;
            }
            StopPythonEngine();
        }


        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void tabPage2_Click(object sender, EventArgs e)
        {

        }

        private void tabPage3_Click(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                openImageText.Hide();
                openImageBtn.Hide();
                stopBtn.Enabled = true;

            }

        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {

            if (radioButton2.Checked)
            {
           

                openImageText.Show();
                openImageBtn.Show();
                stopBtn.Enabled = false;


            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Create an instance of the open file dialog box.
            OpenFileDialog openFileDialog1 = new OpenFileDialog();

            // Set filter options and filter index.
            openFileDialog1.Filter = "JPEG Files (.jpg)|*.jpg|All Files (*.*)|*.*";
            openFileDialog1.FilterIndex = 1;

            openFileDialog1.Multiselect = true;

            // Call the ShowDialog method to show the dialog box.
            DialogResult dialogResult = openFileDialog1.ShowDialog();

            // Process input if the user clicked OK.
            if (dialogResult == System.Windows.Forms.DialogResult.OK)
            {
                openImageText.Text = openFileDialog1.FileName;
 
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }



        private void Run(object parameters)
        {
            ListenerThreadParameters listenerThreadParameters = (ListenerThreadParameters)parameters;
            try
            {
                // Build listener for python engine
                listener = new TcpListener(listenerThreadParameters.port);
                listener.Start();
                //  Wait connection from python engine and if successful then create new socket to python engine
                pythonClient = listener.AcceptTcpClient();
                listenerThreadParameters.mainForm.PrintToLog((DateTime.Now.ToShortTimeString() + " :  Server trying start..."), Color.Black);
                listener.Stop(); // stop listening because python engine connected to GUI
                flagRun = true;
                // Asynchronic StateObject
                StateObject stateObject = new StateObject();
                stateObject.workSocket = pythonClient.Client;
                // Begins to asynchronously receive data from a connected socket with  python engine
                pythonClient.Client.BeginReceive(stateObject.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(Read_Callback), stateObject);
            }
            catch (SocketException se)
            {
                listenerThreadParameters.mainForm.PrintToLog(se.Message, Color.Red);
            }
            catch (Exception e)
            {
                listenerThreadParameters.mainForm.PrintToLog(e.Message, Color.Red);
            }
        }

                private void button3_Click(object sender, EventArgs e)
        {
            pythonListenerThread = new Thread(new ParameterizedThreadStart(Run));
            ListenerThreadParameters parameters = new ListenerThreadParameters();
            parameters.ip = textBoxIP.Text;
            parameters.port = int.Parse(textboxPort.Text);
            parameters.mainForm = this;
            pythonListenerThread.Start(parameters);
            StartPythonEngine();

        }


                public void Read_Callback(IAsyncResult ar)
                {
                    try
                    {
                        // An IAsyncResult that stores state information and any user defined data for this asynchronous operation
                        StateObject stateObject = (StateObject)ar.AsyncState;
                        if (pythonClient != null && flagRun)
                        {
                            // Ends a pending asynchronous read.
                            int read = stateObject.workSocket.EndReceive(ar);

                            if (read > 0)
                            {
                                string msg = Encoding.ASCII.GetString(stateObject.buffer, 0, read);
                                //All of the data has been read, so check out what command

                                string[] items = msg.Split('#');
                                switch (items[0])  // command
                                {
                                    case "Disconnected":
                                        RemoveClient(items[1]);
                                        break;
                                    default:
                                        if (items[0].StartsWith("Connected client"))
                                            AddNewClient(items[0].Split('=')[1]);
                                        PrintToLog(items[0], Color.Blue);
                                        if (items[0].Contains("Aborting the server"))
                                            StopPythonEngine();
                                        break;
                                }
                            }
                            if (flagRun)
                                stateObject.workSocket.BeginReceive(stateObject.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(Read_Callback), stateObject);
                        }
                    }
                    catch (Exception se)
                    {
                        PrintToLog(se.Message, Color.Red);
                        Close();
                    }
                }


                public void RemoveClient(string ip)
                {
                    this.Invoke((MethodInvoker)delegate
                    {
                        int index = connectedIps.Text.IndexOf(ip);
                        if (index != -1)
                        {
                            string newIps = connectedIps.Text;
                            newIps.Remove(index, ip.Length + 1);
                            connectedIps.Text = newIps;
                            PrintToLog("Disconnected client with ip " + ip, Color.Red);
                        }
                    });
                }

                public void AddNewClient(string ip)
                {
                    this.Invoke((MethodInvoker)delegate
                    {
                        connectedIps.Text += ip;
                        connectedIps.Text += "\n";

                        PrintToLog("Connected  client with ip " + ip, Color.Red);
                    });
                }

                public void StopPythonEngine()
                {
                    try
                    {
                        Send("StopAll#");
                        if (pythonEngineProcess != null)
                        {
                            pythonEngineProcess.Kill();
                            pythonEngineProcess.Dispose();
                            pythonEngineProcess = null;
                        }
                            Close();
                    }
                    catch (Win32Exception e)
                    {
                        PrintToLog(e.Message, Color.Red);
                        pythonEngineProcess = null;
                    }
                    catch (InvalidOperationException e)
                    {
                        PrintToLog(e.Message, Color.Red);
                        pythonEngineProcess = null;
                    }
                    catch (Exception e)
                    {
                        PrintToLog(e.Message, Color.Red);
                        pythonEngineProcess = null;
                    }
     
                }

                public void Close()
                {
                    if (pythonClient != null)
                    {
                        pythonClient.Close();
                        pythonClient = null;
                    }
                    flagRun = false;
                    if (pythonListenerThread.IsAlive)
                        pythonListenerThread.Abort();
                    PrintToLog(DateTime.Now.ToShortTimeString() + " :  Server shutdown... ", Color.Black);
                }

                public void Send(string msg)
                {
                    try
                    {
                        if (pythonClient != null)
                            pythonClient.Client.Send(Encoding.ASCII.GetBytes(msg));
                    }
                    catch (Exception e)
                    {
                        Close();
                    }

                }


        public void PrintToLog(string msg, Color color)
        {
            if (this.InvokeRequired)
            {
                this.Invoke((MethodInvoker)delegate
                                {
                                    logBox.SelectionColor = color;
                                    this.logBox.AppendText(msg + Environment.NewLine);
                                    this.logBox.ScrollToCaret();
                                });
            }
            else
            {
                logBox.SelectionColor = color;
                this.logBox.AppendText(msg + Environment.NewLine);
                this.logBox.ScrollToCaret();
            }
        }



        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void startBtn_Click(object sender, EventArgs e)
        {
            if (true)
            //if (connectedIps.Text.Length > 0)
            {
                if (openImageText.Equals(""))
                    MessageBox.Show("Please choose a picture", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                else
                    Send("StartSliceImage#" + openImageText.Text);

            }
            else
            {
                MessageBox.Show("Please Wait for clients to connect", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        }

        
    }
